from scrapy import Spider, Request
from urlscrape.items import UrlscrapeItem


class urlSpider(Spider):
	name = 'url_spider'
	allowed_domains = ['www.the-numbers.com']
	start_urls = ['https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']



	def parse(self,response):

		#List comprehension to construct all the urls of Top Movies at Worldwide Box Office for each year in scope. 
		#Years in scope currently selected: 2019 to 1989
		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]


		for cumulativeurl in page_urls:
			yield Request(url=cumulativeurl, callback=self.parse_results_page)

	def parse_results_page(self, response):

		#This function parses the result page of Top Movies Worldwide Box Office in each year.
		#Specifying the xpath for the href of each individual movie from the table
		
		#Extracting all the individual movie URLs:
		parsemovie_urls = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href').extract()



		for indivmovie_url in parsemovie_urls:
			movie_urls = indivmovie_url

			item = UrlscrapeItem()
			item['movie_urls'] = movie_urls

			yield item


