import scrapy
from scrapy.selector import Selector
import time
import datetime

class LeisuSpider(scrapy.Spider):
    name = 'leisu'
    list_url = 'https://live.leisu.com/wanchang?date=%s'
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
        print('grab data:', start, response.text)
