# _*_ coding: utf-8 _*_
import scrapy
import traceback
import redis
import time
import requests
import re
from lxml import etree
from pyv8.PyV8 import JSContext
from er_shou_che.items import ErShouCheItem
from er_shou_che import citys


class GuaZiSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    start_urls = [
        'https://www.guazi.com/www/i-yage/'
    ]
    base_url = 'https://www.guazi.com'
    store_key = 'urls'
    Cookie = {}
    redis_url = scrapy.utils.project.get_project_settings().get('REDIS_CLIENT', None)
    use_redis = (redis_url != None)
    if use_redis:
        redis_client = redis.StrictRedis.from_url(redis_url)        
    
    def parse(self, response):
        if response.status == 203:
            cookie = self._get_cookie(response.url)
            self.Cookie = cookie
            # print response.body
            yield scrapy.Request(response.url, cookies=cookie, callback=self.parse, dont_filter=True)
        elif response.status == 200:
            # cookie = self._get_cookie(response.url)
            car_urls = response.xpath('//ul[@class="carlist clearfix js-top"]//a//@href')
            urls = [x.extract() for x in car_urls]
            self._store_url(urls)
            next_url = response.xpath(
                '//div[@class="pageBox"]//a[@class="next"]//@href').extract_first()
            if next_url:
            # if False:
                yield scrapy.Request(self.base_url + next_url, cookies=self.Cookie, callback=self.parse)
            else:
                # 开如获取车辆的详细信息
                while self.redis_client.scard(self.store_key) > 0:
                    car_url = self.redis_client.spop(self.store_key)
                    yield scrapy.Request(car_url, cookies=self.Cookie, callback=self.page_carinfo)
                # car_url = self.redis_client.spop(self.store_key)
                # yield scrapy.Request(car_url, cookies=self.Cookie, callback=self.page_carinfo)

    def _store_url(self, urls):
        for url in urls:
            self.redis_client.sadd(self.store_key, self.base_url + url)

    def _get_cookie(self, url):
        r = requests.get(url, headers=scrapy.utils.project.get_project_settings().get(
            'DEFAULT_REQUEST_HEADERS', {}))
        r.encoding = 'utf-8'

        response = etree.HTML(r.text)
        jscontent = response.xpath('//script/text()')

        if jscontent == []:
            time.sleep(70)
            return self._get_cookie(url)
        jscontent = jscontent[0].encode('utf8')
        jscontent = jscontent.replace(
            "xredirect(name,value,url,\'https://\');", "")
        jscontent = jscontent.replace('1C.1c=', 'h ')

        context = JSContext()
        context.enter()
        context.eval(jscontent)
        vars = context.locals
        cookie = vars.xredirect(vars.name, vars.value, vars.url)
        if cookie == '':
            time.sleep(70)
            return self._get_cookie(url)
        result_cookie = dict()
        for c in cookie.split('; '):
            k_v = c.split('=')
            result_cookie[k_v[0]] = k_v[1]

        return result_cookie

    def page_carinfo(self, response):
        item = ErShouCheItem()
        if response.status == 203:
            cookie = self._get_cookie(response.url)
            self.Cookie = cookie
            yield scrapy.Request(response.url, cookies=self.Cookie, callback=self.page_carinfo, dont_filter=True)
        else:
            guanzhu = response.xpath(
                '//div[@class="nav-r"]//i[@class="fc-green"]/text()').extract_first()
            product_textbox = response.xpath('//div[@class="product-textbox"]')
            titlebox = product_textbox.xpath('//h2[@class="titlebox"]')
            title = titlebox.xpath('text()').extract_first()
            title = title.strip() if title else None
            baomai = titlebox.xpath(
                '//span[@class="labels baomai"]/text()').extract_first()
            baoyang = ' '.join([x for x in titlebox.xpath(
                '//span[@class="labels"]/text()').extract()])
            assort = product_textbox.xpath(
                '//ul[@class="assort clearfix"]//li//span/text()').extract()
            assort.extend([]*(4-len(assort)))
            pricebox = product_textbox.xpath('//div[@class="pricebox js-disprice"]')
            price = pricebox.xpath(
                '//span[@class="pricestype"]/text()').extract_first()
            price = price.strip() if price else None
            newcarprice = pricebox.xpath(
                '//span[@class="newcarprice"]/text()').extract_first()
            newcarprice = newcarprice.strip() if newcarprice else None
            desc = response.xpath(
                '//div[@class="test-con"]/text()').extract_first()

            # print guanzhu, title, baomai, baoyang, assort, price, newcarprice, desc
            if title is None:
                yield scrapy.Request(response.url, cookies=self.Cookie, callback=self.page_carinfo, dont_filter=True)
            
            item['title'] = title
            item['guanzhu'] = guanzhu
            item['baomai'] = baomai
            item['baoyang'] = baoyang
            item['shangpai_time'] = assort[0].strip()
            l_c = assort[1].replace(u'万公里', '').strip()
            item['licheng'] = float(l_c) if l_c != '' else None
            item['address'] = assort[2].strip()
            item['province'] = citys.get(item['address'])
            item['pailiang'] = assort[3].strip()
            item['biansuxiang'] = assort[4].strip()
            item['price'] = float(price.replace(u'¥', '').strip())
            new_p = newcarprice.replace(
                u'新车指导价', '').replace(u'万(含税)', '').strip()
            item['newcarprice'] = float(new_p) if new_p != '' else None
            item['desc'] = desc.strip()
            item['url'] = response.url

            yield item
