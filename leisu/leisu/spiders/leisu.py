import scrapy
from scrapy.selector import Selector
import time
import datetime
from leisu.items import LeisuItem

class LeisuSpider(scrapy.Spider):
    name = 'leisu'
    list_url = 'https://live.leisu.com/wanchang?date=%s'
    detail_url = 'https://live.leisu.com/3in1-%s'
    def __init__(self, start=None, end=None, *args, **kwargs):
        super(LeisuSpider, self).__init__(*args, **kwargs)
        self.start = datetime.datetime.strptime(start, "%Y-%m-%d")
        self.end = datetime.datetime.strptime(end, "%Y-%m-%d")
        assert self.start <= self.end
        print("start:", self.start, ",end:", self.end) 

    def start_requests(self):
        start = self.start
        while start <= self.end:
            url = self.list_url % start.strftime("%Y%m%d")
            yield scrapy.Request(url, meta={'time': start}, callback=self.day_list)
            start += datetime.timedelta(days=1)

    def day_list(self, response):
        start = response.meta['time']
        sel = response.xpath
        matchList = [match for match in sel('//li[@data-status="8"]/@data-id').extract()]
        for match in matchList:
            div_sel = sel('//li[@data-id="'+match+'"]/div[@class="find-table layout-grid-tbody hide"]/div[@class="clearfix-row"]').xpath
            league_name = div_sel('span[@class="lab-events"]/a[@class="event-name"]/span/text()').extract()
            jc = div_sel('span[@class="lab-lottery"]/span[@class="text-jc"]/text()').extract()
            home_team = div_sel('*/span[@class="lab-team-home"]/*/a/text()').extract()
            away_team = div_sel('*/span[@class="lab-team-away"]/*/a/text()').extract()
            score = div_sel('*/span[@class="lab-score color-red"]/span[@class="score"]/b/text()').extract()
            item = LeisuItem()
            item['match_time']=start.strftime("%Y%m%d")
            item['jc_order']='' if len(jc)==0 else jc[0].strip()
            item['league']= '' if len(league_name)==0 else league_name[0].strip()
            item['home_team']='' if len(home_team)==0 else home_team[0].strip()
            item['away_team']='' if len(away_team)==0 else away_team[0].strip()
            item['score']='' if len(score)==0 else score[0].strip()
            url = self.detail_url % match
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        sel = response.xpath
        comps = [comp.strip() for comp in sel('//div[contains(@class, "select-company")]/div[@class="down"]/ul/li[not(@class)]/@data-value').extract()]
        odds = {}
        for comp in comps:
            tr = sel('//tr[@data-id="'+comp+'"]/td[contains(@class,"bd-left")]/div[@class="begin float-left w-bar-100 bd-bottom p-b-8 color-999 m-b-8"]/span[@class="float-left col-3"]/text()').extract()
            comp_odd = [odd.strip() for odd in tr]
            check = True
            for odd in comp_odd:
                if odd=='-':
                    check = False
            if check:
                item.save_odd(comp,comp_odd)
        #item['odds']=odds
        #print('item', item)
        yield item

