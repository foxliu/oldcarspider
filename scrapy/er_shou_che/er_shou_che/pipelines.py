# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from er_shou_che.db.dbhelper import CarInfoModel

class ErShouChePipeline(object):
    def process_item(self, item, spider):
        car_info_instance = CarInfoModel()
        car_info_instance.title = item['title']
        car_info_instance.guanzhu = item['guanzhu']
        car_info_instance.baomai = item['baomai']
        car_info_instance.baoyang = item['baoyang']
        car_info_instance.shangpai_time = item['shangpai_time']
        car_info_instance.licheng = item['licheng']
        car_info_instance.address = item['address']
        car_info_instance.province = item['province']
        car_info_instance.pailiang = item['pailiang']
        car_info_instance.biansuxiang = item['biansuxiang']
        car_info_instance.price = item['price']
        car_info_instance.newcarprice = item['newcarprice']
        car_info_instance.desc = item['desc']
        car_info_instance.url = item['url']
        car_info_instance.insert()
