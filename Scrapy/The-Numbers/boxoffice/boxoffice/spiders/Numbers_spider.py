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
		# all 
		# page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]


		###TESTING
		# page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,2017,-1)]
		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']


		for url in page_urls:
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):

		#This function parses the result page of Top Movies Worldwide Box Office in each year.
		#Specifying the xpath for the href of each individual movie from the table
		
		#Extracting all the individual movie URLs:
		movie_urls = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href').extract()


		####Troubleshooting - movie 27, 32, 47, 50, 63, 67, 69, 75, 77, 80, 90, 95
		# tblesht = [27, 32, 47, 50, 63, 67, 69, 75, 77, 80, 90, 95]
		# tblelist = []
		# movie_urls = 
		# for i in tblesht:


		# movie_urls = [f'response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href')[{i}].extract()' for i in tblesht]
		# print('='*55)
		# print(movie_urls)
		# print('='*55)

		#####

		#Convert Xpath of individual movie_urls to actual web address
		movie_urls = [f'https://www.the-numbers.com/{url}' for url in movie_urls]


		#Yield the request to each individual movie's page
		for url in movie_urls:
			yield Request(url=url, callback=self.parse_movie_page)


	def parse_movie_page(self, response):

		#Once within the individual movie pages:


		movie_info = response.xpath('//div[@id="main"]')

		for movie in movie_info:

			movie_title = 'DNE'
			domestic_box = 'DNE'
			international_box = 'DNE'
			worldwide_box = 'DNE'
			production_budget = 'DNE'
			domestic_release = 'DNE'
			MPAA_rating = 'DNE'
			running_time = 'DNE'
			source = 'DNE'
			genre = 'DNE'
			production_method = 'DNE'
			creative_type = 'DNE'
			production_country = 'DNE'
			language = 'DNE'
			# alltime_rank = 'DNE'
			# year_rank = 'DNE'

			if movie_info.xpath('div[@itemtype="https://schema.org/Movie"]') != []:
				#Parse for movie title
				movie_title = movie_info.xpath('.//div/h1/text()').extract_first()
				print('='*55)
				print(movie_title)
				print('='*55)

			else:
				#Parse for movie titles if different web format
				print("*"*55)
				print('This is one of the exceptions')
				print("*"*55)
				print(movie_info.xpath('.//h1/text()').extract_first())
				movie_title = movie_info.xpath('.//h1/text()').extract_first()

			# try:
						

			# except:


			#Parse for domestic box office
			domestic_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data"]/text()').extract_first()
			print('='*55)
			print(domestic_box)
			print('='*55)

			#Parse for international box office
			international_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data sum"]/text()').extract_first()
			print('='*55)
			print(international_box)
			print('='*55)

			#Parse for worldwide box office
			worldwide_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr[4]/td[@class="data"]/text()').extract_first()
			print('='*55)
			print(worldwide_box)
			print('='*55)


			# Xpath for "Metrics" : response.xpath('.//div[@id="summary"]/table[1]/tr//text()').extract()
				# Xpath for "[Production Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td/b/text()').extract_first()
				# Xpath for "[Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td[2]/text()').extract_first()
				# //*[@id="summary"]/table[1]/tbody/tr[4]/td[2]

			if movie_info.xpath('.//*[@id="summary"]//table[1]/tr[4]/td/b/text()').extract_first() == 'Production\xa0Budget:':
				production_budget = movie_info.xpath('.//div/*[@id="summary"]//table[1]/tr[4]/td[2]/text()').extract_first()
				print('='*55)
				print('the production budget is ' + str(production_budget))
				print('='*55)

				# try:

				

				# except

			#If no production budget is given on the website, input as "N/A"
			else:
				production_budget = 'N/A'
				print('='*55)
				print('No production budget')
				print('='*55)

			# Xpath for "Movie Details" table: response.xpath('.//div[@id="summary"]/table[2]/tr//text()').extract()
			#
			moviedetails_table = movie_info.xpath('.//*[@id="summary"]/table[2]//tr')
			
			#Parsing within the "Movie Details" table
			#Loop through each Selector in the Movie Details table to find specific headers to extract values
			for moviedetail_tr in moviedetails_table:
				#Define the Selectors for ease of reference
				detail_heading = moviedetail_tr.xpath('./td/b/text()').extract_first()


				#Parse for release date
				if detail_heading == 'Domestic Releases:':
					domestic_release = moviedetail_tr.xpath('./td/text()').extract_first()
					print('='*55)
					print('the release date is ' + str(domestic_release))
					print('='*55)

					# try:


					# except:

				#Parse for MPAA rating
				if detail_heading == 'MPAA\xa0Rating:':
					MPAA_rating = moviedetail_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('the rating is ' + str(MPAA_rating))
					print('='*55)

				#Parse for running time
				if detail_heading == 'Running Time:':
					running_time = moviedetail_tr.xpath('./td[2]/text()').extract_first()
					print('='*55)
					print('the running_time is ' + str(running_time))
					print('='*55)

				#Parse for source
				if detail_heading == 'Source:':
					source = moviedetail_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('the source is ' + str(source))
					print('='*55)


				#Parse for the genre value
				if detail_heading == 'Genre:':
				# xpath('.//*[@id="summary"]/table[2]//tr/td/b/text()')
					genre = moviedetail_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('the genre is ' + str(genre))
					print('='*55)


				#Parse for the Production Method
				if detail_heading == 'Production\xa0Method:':
					production_method = moviedetail_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('the production method is ' + str(production_method))
					print('='*55)


				#Parse for Creative Type
				if detail_heading == 'Creative\xa0Type:':
					creative_type = moviedetail_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('the creative_type is ' + str(creative_type))
					print('='*55)


				#Parse for the Production Countries (may have more than one)
				if detail_heading == 'Production Countries:':
					production_country = moviedetail_tr.xpath('./td/a//text()').extract()
					print('='*55)
					print('the production country is ' + str(production_country))
					print('='*55)


				# Parse for the Language (may have more than one)
				if detail_heading == 'Languages:':
					language = moviedetail_tr.xpath('./td/a//text()').extract()
					print('='*55)
					print('the language is ' + str(language))
					print('='*55)


				# Parse for All Time Ranking
				# if detail_heading == '':
				# 	alltime_rank = 


				# Parse for Year Ranking
				# if detail_heading == :
				# 	year_rank = 

				#If there are any of the fields where the information is not provided:
				# else:
				# 	genre = 'Not available'
				# 	print('='*55)
				# 	print('No genre')
				# 	print('='*55)



			item = BoxofficeItem()
			item['movie_title'] = movie_title
			item['domestic_box'] = domestic_box
			item['international_box'] = international_box
			item['worldwide_box'] = worldwide_box
			item['production_budget'] = production_budget
			item['domestic_release'] = domestic_release
			item['MPAA_rating'] = MPAA_rating
			item['running_time'] = running_time
			item['source'] = source
			item['genre'] = genre
			item['production_method'] = production_method
			item['creative_type'] = creative_type
			item['production_country'] = production_country
			item['language'] = language
			# item['alltime_rank'] = alltime_rank
			# item['year_rank'] = year_rank

			yield item





