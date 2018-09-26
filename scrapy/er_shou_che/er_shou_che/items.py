# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErShouCheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   title = scrapy.Field()
   guanzhu = scrapy.Field()
   baomai = scrapy.Field()
   baoyang = scrapy.Field()
   shangpai_time = scrapy.Field()
   licheng  = scrapy.Field()
   address = scrapy.Field()
   province = scrapy.Field()
   pailiang = scrapy.Field()
   biansuxiang = scrapy.Field()
   price = scrapy.Field()
   newcarprice = scrapy.Field()
   desc = scrapy.Field()
   url = scrapy.Field()
