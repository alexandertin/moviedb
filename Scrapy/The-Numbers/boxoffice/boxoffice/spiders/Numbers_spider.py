from scrapy import Spider
from boxoffice.items import BoxofficeItem


class BoxOfficeSpider(Spider):
	name = 'boxoffice_spider'
	allowed_domains = ['https://www.the-numbers.com/']
	start_urls = ['https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']


	def parse(self,response):

		#define the number of 

		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]

		for url in page_urls:
			yield Request(url=url, callback=self.parse_results_page)


	def parse_results_page(self, response):

		rows = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr')


	def parse_movie_page(self, response):

		#once within the individual movie pages, 

		ind_movie_url = response.xpath('//div[@id="main"]')

		# Checkpoint 1: This is for testing purposes
		# print('='*55)
		# print(len(product_urls))
		# print('='*55)

		for movie in ind_movie_url:
			movie_title = movie.xpath('./div/h1/text()').extract_first()
			domestic_box = movie.xpath('./div/table[@id="movie_finances"]/tr/td[@class="data"]/text()').extract_first()
			international_box = movie.xpath('./div/table[@id="movie_finances"]/tr/td[@class="data sum"]/text()').extract_first()
			worldwide_box = movie.xpath('./div/table[@id="movie_finances"]/tr[4]/td[@class="data"]/text()').extract_first()
			production_budget = movie.xpath('./div/table[@id="summary"]/table/tbody/tr[4]/td[2]/text()').extract_first()
			international_release = movie.
			release_date = movie.
			MPAA_rating = movie.
			running_time = movie.
			franchise = movie.
			keywords = movie.
			genre = movie.
			production_method = movie.
			creative_type = movie.
			production_country = movie.
			language = movie.

			item = BoxofficeItem()
			item['movie_title'] = 






