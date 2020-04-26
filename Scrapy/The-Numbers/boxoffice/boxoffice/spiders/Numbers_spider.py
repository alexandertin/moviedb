from scrapy import Spider, Request
from boxoffice.items import BoxofficeItem

class BoxOfficeSpider(Spider):
	name = 'boxoffice_spider'
	allowed_domains = ['www.the-numbers.com']
	start_urls = ['https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019']


	def parse(self,response):

		#List comprehension to construct all the urls of Top Movies at Worldwide Box Office for each year in scope. 
		#Years in scope currently selected: 2019 to 1989

		page_urls = [f'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{i}' for i in range(2019,1988,-1)]


		for url in page_urls:
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):

		#This function parses the result page of Top Movies Worldwide Box Office in each year.
		#Specifying the xpath for the href of each individual movie from the table
		
		#Extracting all the individual movie URLs:
		movie_urls = response.xpath('//*[@id="page_filling_chart"]/center/table/tbody/tr/td//@href').extract()


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

		movie_title = movie_info.xpath('.//h1/text()').extract_first()

		#Extract domestic box office
		domestic_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data"]/text()').extract_first()


		#Extract for international box office
		international_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr/td[@class="data sum"]/text()').extract_first()
	

		#Extract for worldwide box office
		worldwide_box = movie_info.xpath('.//div/table[@id="movie_finances"]/tr[4]/td[@class="data"]/text()').extract_first()



		#Xpath for the Summary tab
		summary_tab = movie_info.xpath('.//*[@id="summary"]') #entire tab, so just 1 selector
		sumtab_selectors = summary_tab.xpath('./table//tr') # selectors for all rows in summary tab
		sumtab_headers = sumtab_selectors.xpath('.//td/b/text()') # path for row value - looking for 'Production\xa0Budget:' and the corresponding value

		# For loop each of the selector in summary tab to find the Production Budget Row.
		for summaryselector in sumtab_selectors:
			#If it is the "Production Budget" row:
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Production\xa0Budget:':
				production_budget = summaryselector.xpath('./td/text()').extract_first()
	
			#Extract release date
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Domestic Releases:':
				domestic_release = summaryselector.xpath('./td/text()').extract_first()


			#Extract MPAA rating
			if summaryselector.xpath('./td/b/text()').extract_first() == 'MPAA\xa0Rating:':
				MPAA_rating = summaryselector.xpath('./td/a/text()').extract_first()


			#Extract running time
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Running Time:':
				running_time = summaryselector.xpath('./td/text()').extract_first()

			#Extract source
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Source:':
				source = summaryselector.xpath('./td/a/text()').extract_first()


			#Extract genre value
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Genre:':
			# xpath('.//*[@id="summary"]/table[2]//tr/td/b/text()')
				genre = summaryselector.xpath('./td/a/text()').extract_first()

			#Extract the Production Method
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Production\xa0Method:':
				production_method = summaryselector.xpath('./td/a/text()').extract_first()

			#Extract Creative Type
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Creative\xa0Type:':
				creative_type = summaryselector.xpath('./td/a/text()').extract_first()


			#Extract the Production Countries (may have more than one)
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Production Countries:':
				production_country = summaryselector.xpath('./td/a/text()').extract()



			# Extract for the Language (may have more than one)
			if summaryselector.xpath('./td/b/text()').extract_first() == 'Languages:':
				language = summaryselector.xpath('./td/a/text()').extract()



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

		yield item

