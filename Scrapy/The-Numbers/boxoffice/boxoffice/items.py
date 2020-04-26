# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxofficeItem(scrapy.Item):
	
	movie_title = scrapy.Field()
	domestic_box = scrapy.Field()
	international_box = scrapy.Field()
	worldwide_box = scrapy.Field()
	production_budget = scrapy.Field()
	domestic_release = scrapy.Field()
	MPAA_rating = scrapy.Field()
	running_time = scrapy.Field()
	source = scrapy.Field()
	genre = scrapy.Field()
	production_method = scrapy.Field()
	creative_type = scrapy.Field()
	production_country = scrapy.Field()
	language = scrapy.Field()


