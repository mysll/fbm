from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'leisu', '-a', 'start=2020-06-01', 
         '-a', 'end=2020-06-30', '-o', 'odd-202006.csv'])
