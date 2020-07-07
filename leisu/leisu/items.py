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
    #竞彩场次
    jc_order = scrapy.Field()
    league = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    score = scrapy.Field()
    odds = scrapy.Field()
    #2
    bet365 = scrapy.Field()
    #3 皇冠
    hg = scrapy.Field()
    #4 10BET
    bet10 = scrapy.Field()
    #5 立博
    lb = scrapy.Field()
    #6 明陞
    ms = scrapy.Field()
    #7 澳彩
    ac = scrapy.Field()
    #8 SNAI
    snai = scrapy.Field()
    #9 威廉希尔
    wl = scrapy.Field()
    #10 易胜博
    ysb = scrapy.Field()
    #11 韦德
    wd = scrapy.Field()
    #13 Inter wetten
    iw = scrapy.Field()
    #14 12bet
    bet12 = scrapy.Field()
    #15 利记
    lj = scrapy.Field()
    #16 盈禾
    yh = scrapy.Field()
    #17 18Bet
    bet18 = scrapy.Field()
    #19 竞彩官方
    jc = scrapy.Field()
    #21 188
    ybb = scrapy.Field()
    #22 平博
    pb = scrapy.Field()

    def save_odd(self, id, data):
        if id == '2':
            self['bet365']=data
        elif id == '3':
            self['hg']=data
        elif id == '4':
            self['bet10']=data
        elif id == '5':
            self['lb']=data
        elif id == '6':
            self['ms']=data
        elif id == '7':
            self['ac']=data
        elif id == '8':
            self['snai']=data
        elif id == '9':
            self['wl']=data
        elif id == '10':
            self['ysb']=data
        elif id == '11':
            self['wd']=data
        elif id =='13':
            self['iw']=data
        elif id == '14':
            self['bet12']=data
        elif id == '15':
            self['lj']=data
        elif id == '16':
            self['yh']=data
        elif id == '17':
            self['bet18']=data
        elif id == '19':
            self['jc']=data
        elif id =='21':
            self['ybb']=data
        elif id == '22':
            self['pb']=data


