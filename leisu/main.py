from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'leisu', '-a', 'start=2020-07-01', 
         '-a', 'end=2020-07-01'])
