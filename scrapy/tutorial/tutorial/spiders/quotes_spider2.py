import scrapy

class QuotesSpider(scrapy.Spider):
	name="quotes2"
	start_urls=['http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',]
	def parse(self,response):
		for quote in response.css('div.quote'):
			yield{
		'text':quote.css('span.text::text').extract_first(),
		'author':quote.css('span small::text').extract_first(),
		'tag':quote.css('div.tags a.tag::text').extract_first(),
		}
		next_page=response.css('li.next a::attr(href)').extract_first()
		if next_page is not None:
			next_page=response.urljoin(next_page)
			print('+++next page is ' +next_page)
			yield scrapy.Request(url=next_page,callback=self.parse)
