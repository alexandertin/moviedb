from scrapy import Spider
from scrapy import Request
from boxoffice.items import BoxofficeItem
import re

class BoxOfficeSpider(Spider):
	name = 'boxoffice_spider'
	allowed_domains = ['www.the-numbers.com']
	start_urls = ['https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']


	# year_in_scope = range(2019,1988,-1)

	def parse(self,response):

		#List comprehension to construct all the urls of Top Movies at Worldwide Box Office for each year in scope. 
		#Years in scope currently selected: 2019 to 1989
		# all 

		# page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]


		###TESTING
		# page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,2017,-1)]
		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-1994']


		for url in page_urls:
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):

		#This function parses the result page of Top Movies Worldwide Box Office in each year.
		#Specifying the xpath for the href of each individual movie from the table
		
		#Extracting all the individual movie URLs:
		movie_urls = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href').extract()



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

		"""
		#Once within the individual movie pages, there are three sub cateogries to dig into.
		1) The movie title at the top

		2) Theatrical performance table (Domestic_box, International_box, Worldwide_Box)

		3) Metrics table (Production Budget)

		4) Movie details table ()

		5) Worldwide Cumulative Box Office Records table ()

		"""
		#Movie Page highest level 
		movie_info = response.xpath('//div[@id="main"]')

		for movie in movie_info: #NOT NECESSARY(?)

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
			alltime_rank = 'DNE'
			year_rank = 'DNE'



			movie_title = movie_info.xpath('.//h1/text()').extract_first()


			#--- Original --- (but doesn't seem necessary)
			# if movie_info.xpath('div[@itemtype="https://schema.org/Movie"]') != []:
			# 	#Extract movie title
			# 	movie_title = movie_info.xpath('.//div/h1/text()').extract_first()
			# 	print('='*55)
			# 	print(movie_title)
			# 	print('='*55)

			# else:
			# 	#Extract movie titles if different web format
			# 	print(movie_info.xpath('.//h1/text()').extract_first())
			# 	movie_title = movie_info.xpath('.//h1/text()').extract_first()


			#Extract domestic box office
			domestic_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data"]/text()').extract_first()
			# print('='*55)
			# print(domestic_box)
			# print('='*55)

			#Extract for international box office
			international_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data sum"]/text()').extract_first()
			# print('='*55)
			# print(international_box)
			# print('='*55)

			#Extract for worldwide box office
			worldwide_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr[4]/td[@class="data"]/text()').extract_first()
			# print('='*55)
			# print(worldwide_box)
			# print('='*55)


			# Xpath for "Metrics" : response.xpath('.//div[@id="summary"]/table[1]/tr//text()').extract()
				# Xpath for "[Production Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td/b/text()').extract_first()
				# Xpath for "[Budget]": response.xpath('.//div[@id="summary"]/table[1]/tr[4]/td[2]/text()').extract_first()
				# //*[@id="summary"]/table[1]/tbody/tr[4]/td[2]

			"""
			Lower table with tabs now

			"""

			summary_tab = movie_info.xpath('.//*[@id="summary"]') #entire tab, so just 1 selector
			sumtab_selectors = summary_tab.xpath('./table//tr') # selectors for all rows in summary tab
			sumtab_headers = sumtab_selectors.xpath('.//td/b/text()') # path for row value - looking for 'Production\xa0Budget:' and the corresponding value

			international_tab = movie_info.xpath('.//*[@id="international"]') #entire international tab, so just 1 selector
			intltab_selectors = international_tab.xpath('.//div//tr/td//text()') #contains selectors will all values in interational tab, now use for loop

			# For loop each of the selector in summary tab to find the Production Budget Row.
			for summaryselector in sumtab_selectors:
				#If it is the "Production Budget" row:
				if summaryselector.xpath('.//td/b/text()').extract_first() == 'Production\xa0Budget:':
						production_budget = summaryselector.xpath('.//td/text()').extract_first()
			

			# # Xpath for "Movie Details" table: response.xpath('.//div[@id="summary"]/table[2]/tr//text()').extract()
			

			# 		# If it is the "Movie Details" table:
			# 	if :
						
			# 		moviedetails_table = movie_info.xpath('.//*[@id="summary"]/table[2]//tr')
			
			# 		#Extract within the "Movie Details" table
			# 		#Loop through each Selector in the Movie Details table to find specific headers to extract values
			# 		for moviedetail_tr in moviedetails_table:
			# 			#Define the Selectors for ease of reference
			# 			detail_heading = moviedetail_tr.xpath('./td/b/text()').extract_first()


				#Extract release date
				if detail_heading == 'Domestic Releases:':
					domestic_release = moviedetail_tr.xpath('./td/text()').extract_first()
					# print('='*55)
					# print('the release date is ' + str(domestic_release))
					# print('='*55)


				#Extract MPAA rating
				if detail_heading == 'MPAA\xa0Rating:':
					MPAA_rating = moviedetail_tr.xpath('./td/a/text()').extract_first()
					# print('='*55)
					# print('the rating is ' + str(MPAA_rating))
					# print('='*55)

				#Extract running time
				if detail_heading == 'Running Time:':
					running_time = moviedetail_tr.xpath('./td[2]/text()').extract_first()
					# print('='*55)
					# print('the running_time is ' + str(running_time))
					# print('='*55)

				#Extract source
				if detail_heading == 'Source:':
					source = moviedetail_tr.xpath('./td/a/text()').extract_first()
					# print('='*55)
					# print('the source is ' + str(source))
					# print('='*55)


				#Extract genre value
				if detail_heading == 'Genre:':
				# xpath('.//*[@id="summary"]/table[2]//tr/td/b/text()')
					genre = moviedetail_tr.xpath('./td/a/text()').extract_first()
					# print('='*55)
					# print('the genre is ' + str(genre))
					# print('='*55)


				#Extract the Production Method
				if detail_heading == 'Production\xa0Method:':
					production_method = moviedetail_tr.xpath('./td/a/text()').extract_first()
					# print('='*55)
					# print('the production method is ' + str(production_method))
					# print('='*55)


				#Extract Creative Type
				if detail_heading == 'Creative\xa0Type:':
					creative_type = moviedetail_tr.xpath('./td/a/text()').extract_first()
					# print('='*55)
					# print('the creative_type is ' + str(creative_type))
					# print('='*55)


				#Extract the Production Countries (may have more than one)
				if detail_heading == 'Production Countries:':
					production_country = moviedetail_tr.xpath('./td/a//text()').extract()
					# print('='*55)
					# print('the production country is ' + str(production_country))
					# print('='*55)


				# Extract for the Language (may have more than one)
				if detail_heading == 'Languages:':
					language = moviedetail_tr.xpath('./td/a//text()').extract()
					# print('='*55)
					# print('the language is ' + str(language))
					# print('='*55)




				#Above
				# Individual Page: movie_info = response.xpath('//div[@id="main"]')
				# Summary table: moviedetails_table = movie_info.xpath('.//*[@id="summary"]/table[2]//tr')
				# Bold Value: detail_heading = moviedetail_tr.xpath('./td/b/text()').extract_first()

				#============================================================================

				# Below
				# Individual Page: movie_info = response.xpath('//div[@id="main"]')
				# World Cumulative Box Office Records Table: movierank_table = movie_info.xpath('.//*[@id="international"]//div[3]//tr')
				# For loop selector level - detail_heading = movierank_table[1].xpath('./td/a/text()').extract_first()
				# All Time Worldwide Box Office:  movie_info.xpath('.//*[@id="international"]//div[3]//tr[2]//text()')
				#
				# //*[@id="international"]
				#/html/body/div[1]/div[5]/div/div[7]
				# Specific bold value: 

			#Check that is the "Worldwide Cumulative Box Office Records" table:
			if :

			#Specifying the Xpath for a different table on the movies page - Skipping first row as the "key" (Record, Rank Revenue)
			movierank_table = movie_info.xpath('.//*[@id="international"]/div[3]//tr')[1:]
			print('='*55)
			print(len(movierank_table))
			print('='*55)

				# For each Selector in the table containing the rank
				for movierank_tr in movierank_table:
				

					#Implement for loop to check the heading of the actual table?







					#Defining the value check for the right row to extract
					fin_heading = movierank_tr.xpath('./td/a/text()').extract_first()
					print('='*55)
					print('Iterate through the for loop')
					print(fin_heading)
					print('='*55)	

					
					# Option 1:
					# # Extract All Time Ranking
					# if detail_heading == 'All Time Worldwide Box Office':
					# 	alltime_rank = movierank_tr.xpath('./td/text()').extract_first()
					# 	print('='*55)
					# 	print('the all time rank is ' + str(alltime_rank))
					# 	print('='*55)			

					# 	#try to convert to integer

					# Option 2:
					print('*'* 55)
					print(alltime_rank)
					print(alltime_rank == 'DNE')
					print('*'* 55)

					# Extract All Time Ranking
					if  alltime_rank == 'DNE':
						alltime_rank = movierank_tr.xpath('./td/text()').extract_first()
						print('='*55)
						print('all time rank is ' + str(alltime_rank))
						print('='*55)

						# try:
						# 	alltime_rank = int(alltime_rank)
						# except:
						# 	alltime_rank = movierank_tr.xpath('./td/text()').extract_first()
						# print('='*55)
						# print(detail_heading)
						# print(alltime_rank)
						# # print(type(alltime_rank))
						# print('='*55)


					# Extract Year Ranking
					if re.search(f'Top 2019 Movies',detail_heading) != None:
						print('entered year rank')
						year_rank = movierank_tr.xpath('./td/text()').extract_first()
						# try:
						# 	year_rank = int(year_rank)
						# except:
						# 	year_rank = movierank_tr.xpath('./td/text()').extract_first()
						print('='*55)
						print(detail_heading)
						print('the year rank is ' + str(year_rank))
						# print(type(year_rank))
						print('='*55)



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
			item['alltime_rank'] = alltime_rank
			item['year_rank'] = year_rank

			yield item





