# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MyscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class BaiduImgsItem(scrapy.Item):
    title = Field()
    image_url = Field()
    images = Field()
    image_paths =Field()
    desc = Field()
