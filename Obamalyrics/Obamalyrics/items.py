# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ObamalyricsItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	artist = scrapy.Field()
	song = scrapy.Field()
	lyrics = scrapy.Field()
