from scrapy import Spider
from scrapy import Request
from boxoffice.items import BoxofficeItem
import re

class BoxOfficeSpider(Spider):
	name = 'boxoffice_spider'
	allowed_domains = ['www.the-numbers.com']
	start_urls = ['https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']


	def parse(self,response):

		#List comprehension to construct all the urls of Top Movies at Worldwide Box Office for each year in scope. 
		#Years in scope currently selected: 2019 to 1989
		# all page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]

		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,2017,-1)]
		
		print('='*55)
		print(page_urls)
		print('='*55)


		for url in page_urls:
			print(url)
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):

		print('enter parse_results_page')
		#This function parses the result page of Top Movies Worldwide Box Office in each year.
		#Specifying the xpath for the href of each individual movie from the table
		movie_urls = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href').extract()

		#Checkpoint - 
		print('='*55)
		print(len(movie_urls))
		print('='*55)

		####include rank? (using meta)
		# rank = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr//td[@class="data"]/text()').extract()
		
		#convert xpath of movie_urls to actual web address
		movie_urls = [f'https://www.the-numbers.com/{url}' for url in movie_urls]


		#Yield the request to each individual movie's page
		for url in movie_urls:
			yield Request(url=url, callback=self.parse_movie_page)


	def parse_movie_page(self, response):

		#Once within the individual movie pages, 

		movie_info = response.xpath('//div[@id="main"]')



		for movie in movie_info:
			movie_title = movie_info.xpath('.//div/h1/text()').extract_first()
			domestic_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data"]/text()').extract_first()
			international_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data sum"]/text()').extract_first()
			worldwide_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr[4]/td[@class="data"]/text()').extract_first()
			
			# Xpath for "Metrics" : response.xpath('.//div[@id="summary"]/table[1]/tr//text()').extract()
				# Xpath for "[Production Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td/b/text()').extract_first()
				# Xpath for "[Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td[2]/text()').extract_first()
			

			if movie_info.xpath('.//div[@id="summary"]/table[1]/tr[4]/td/b/text()').extract_first() == 'Production\xa0Budget:':
				production_budget = movie_info.xpath('.//div/table[@id="summary"]/table/tr[4]/td[2]/text()').extract_first()
			else:
				print('No production budget')
				production_budget = 'N/A'

			# Xpath for "Movie Details": response.xpath('.//div[@id="summary"]/table[2]/tr//text()').extract()
				# Xpath for
			
			# international_release = movie_info.xpath()
			if movie_info.xpath('.//div[@id="summary"]/table[2]/tr[3]//text()').extract_first() == 'Video\xa0Release:':
				release_date = movie_info.xpath('.//div[@id="summary"]/table[2]/tr[3]/td[2]/text()').extract_first()
			else:
				print('No release date')
				release_date = 'N/A'
			# MPAA_rating = movie_info.
			# running_time = movie_info.
			# franchise = movie_info.
			# keywords = movie_info.
			# genre = movie_info.
			# production_method = movie_info.
			# creative_type = movie_info.
			# production_country = movie_info.
			# language = movie_info.

			item = BoxofficeItem()
			item['movie_title'] = movie_title
			item['domestic_box'] = domestic_box
			item['international_box'] = international_box
			item['worldwide_box'] = worldwide_box
			# item['production_budget'] = production_budget
			# item['international_release'] = international_release
			# item['release_date'] = release_date
			# item['MPAA_rating'] = MPAA_rating
			# item['running_time'] = running_time
			# item['franchise'] = franchise
			# item['keywords'] = keywords
			# item['genre'] = genre
			# item['production_method'] = production_method
			# item['creative_type'] = creative_type
			# item['production_country'] = production_country
			# item['language'] = language

			yield item





