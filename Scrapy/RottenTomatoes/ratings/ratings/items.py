# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RatingsItem(scrapy.Item):

	movie_name = scrapy.Field()
	critic_score = scrapy.Field()
	count_critic_review = scrapy.Field()
	certified_status = scrapy.Field()
	user_score = scrapy.Field()
	count_user_review = scrapy.Field()
