# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeisuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    match_time = scrapy.Field()
    jc = scrapy.Field()
    league = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    score = scrapy.Field()
    odds = scrapy.Field()
