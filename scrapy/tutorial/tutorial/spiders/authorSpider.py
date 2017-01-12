import scrapy

class AuthorSpider(scrapy.Spider):
	name='author'
	start_urls=['http://quotes.toscrape.com/',]
	def parse(self,response):
		for href in response.css('.author+a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href),callback=self.authorParse)
		next_page=response.css('li.next a::attr(href)').extract_first()
		if next_page is not None:
			next_page=response.urljoin(next_page)
			yield scrapy.Request(next_page,callback=self.parse)
	def authorParse(self,response):
		return {
		'author' : response.css('h3.author-title::text').extract_first(),
		'born' : response.css('.author-born-date::text').extract_first(),
		'description' : response.css('.author-description::text').extract_first(),
		}
