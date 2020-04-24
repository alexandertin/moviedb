# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxofficeItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	
	movie_title = scrapy.Field()
	# domestic_box = scrapy.Field()
	international_box = scrapy.Field()
	worldwide_box = scrapy.Field()
	# production_budget = scrapy.Field()
	# international_release = scrapy.Field()
	# release_date = scrapy.Field()
	# MPAA_rating = scrapy.Field()
	# running_time = scrapy.Field()
	# franchise = scrapy.Field()
	# keywords = scrapy.Field()
	# genre = scrapy.Field()
	# production_method = scrapy.Field()
	# creative_type = scrapy.Field()
	# production_country = scrapy.Field()
	# language = scrapy.Field()


