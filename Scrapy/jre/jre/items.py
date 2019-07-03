# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JreItem(scrapy.Item):
    # define the fields for your item here like:
    ep_title = scrapy.Field()
    airdate = scrapy.Field()
    runtime = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    views = scrapy.Field()
    ratio = scrapy.Field()




