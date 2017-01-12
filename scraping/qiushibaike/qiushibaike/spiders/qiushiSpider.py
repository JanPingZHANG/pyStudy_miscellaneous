#coding=utf-8
from scrapy.selector import Selector
from scrapy import Spider
import scrapy
import time

count = 0
class QiushiSpider(Spider):
	name='qiushi'
	start_urls = ['http://www.qiushibaike.com/hot']
	def parse(self,response):
		global count
		authors=response.xpath('//*[@class="article block untagged mb15"]/a[1]/div/span')  
		for author in authors:
			#print '--------'
			st = author.extract()
			st = st.replace('<span>','')
			st = st.replace('</span>','')
			st = st.replace('<br>','\n')
			#print st
			data = open('test.txt','a')
			data.write('\n-----------------------\n')
			data.write(st.encode('utf-8'))
			data.close()
			yield{
				'author':st,
			}

		nextPage = response.xpath('//*[@id="content-left"]/ul/li[last()]/a/@href').extract_first()
		count = count +1
		time.sleep(3)
		if nextPage is not None:
			nextPage = response.urljoin(nextPage)
			print count,' page is: ',nextPage
			yield scrapy.Request(nextPage,callback=self.parse)

