from scrapy import Spider, Request
from ratings.items import RatingsItem


class RottenTomatesSpider(Spider):
	name = 'rotten_spider'
	allowed_domains = ['wwww.rottentomatoes.com']
	start_urls = ['https://www.rottentomatoes.com/m']


	def parse(self, response):


		page_urls = [f'https://www.rottentomatoes.com/m{i}' for i in TO_BE_DEFINED]


		for url in page_urls:
			yield Request(url=url, callback=self.parse_movie_page)

	def parse_movie_page(self,response):

		# Selector containing all the necessary information (Top Level)
		movie_ratings = response.xpath('//*[@id="topSection"]/div[2]/div[1]')

		# //*[@id="topSection"]/div[2]
		movie_name = 'DNE'
		critic_score = 'DNE'
		count_critic_review = 'DNE'
		certified_status = 'DNE'
		user_score = 'DNE'
		count_user_review = 'DNE'


		#Extract the movie name
		movie_name = movie_ratings.xpath('./h1/text()').extract_first()
		print('+'*55)
		print(movie_name)
		print('+'*55)

		#Selector for the box containing the critic review and user reviews
		consensus_box = movie_ratings.xpath('./section/section')

		# Extract the overall critic score
		critic_score = consensus_box.xpath('.//*[@id="tomato_meter_link"]/span[2]/text()').extract_first()
		try:
			critic_score = str.strip(consensus_box.xpath('.//*[@id="tomato_meter_link"]/span[2]/text()').extract_first())
		except: 
			print(f'Sorry mate, could not strip the string')
			critic_score = consensus_box.xpath('.//*[@id="tomato_meter_link"]/span[2]/text()').extract_first()
		print('+'*55)
		print(critic_score)
		print('+'*55)

		#Extract the number of critic reviews
		count_critic_review = consensus_box.xpath('./div[1]/div/small/text()').extract_first()
		try:
			count_critic_review = str.strip(consensus_box.xpath('./div[1]/div/small/text()').extract_first())
		except:
			count_critic_review = consensus_box.xpath('./div[1]/div/small/text()').extract_first()
		print('+'*55)
		print(count_critic_review)
		print('+'*55)

		#Specific class tag for website to exhibit tomato symbol
		certification_tag = consensus_box.xpath('.//*[@id="tomato_meter_link"]/span[1]/@class').extract()
		
		#If it is a "certified fresh", it will show in the tag. This tests if the class tag "certified fresh" is true
		if certification_tag = ['mop-ratings-wrap__icon meter-tomato icon big medium-xs certified_fresh']:
			certified_status = 'Certified Fresh'
			print('+'*55)
			print(certified_boolean)
			print('+'*55)
		#If it is a "fresh", it will show in the tag. This tests if the class tag "fresh" is true
		elif certification_tag = ['mop-ratings-wrap__icon meter-tomato icon big medium-xs fresh']:
			certified_status = 'Fresh'
		#If it is not "certified fresh"or "fresh", should be rotten. This tests if the class tag rotten is true
		elif certification_tag = ['mop-ratings-wrap__icon meter-tomato icon big medium-xs rotten']:
			certified_status = 'Rotten'
		else:
			print('*'*55)
			print('There is no certified status (Error!!!)')
			print('*'*55)

		#Extract the overall user score
		user_score = consensus_box.xpath('./div[2]/h2/a/span[2]/text()').extract_first()
		try:
			user_score = str.strip(consensus_box.xpath('./div[2]/h2/a/span[2]/text()').extract_first())
		except:
			user_score = consensus_box.xpath('./div[2]/h2/a/span[2]/text()').extract_first()

		print('+'*55)
		print(user_score)
		print('+'*55)

		count_user_review = consensus_box.xpath('./div[2]/div/strong/text()').extract_first()
		print('+'*55)
		print(count_user_review)
		print('+'*55)


		item = RatingsItem()
		item['movie_name'] = movie_name
		item['critic_score'] = critic_score
		item['count_critic_review'] = count_critic_review
		item['certified_status'] = certified_status
		item['user_score'] = user_score
		item['count_user_review'] = count_user_review

		yield item







