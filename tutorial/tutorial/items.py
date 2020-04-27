# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    URL = scrapy.Field()   #存放当前网页地址
    TITLE = scrapy.Field() #存放当前网页title
    H1 = scrapy.Field() #存放一级标题
    TEXT = scrapy.Field() #存放正文
