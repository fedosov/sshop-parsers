# -*- coding: utf-8 -*-
__AUTHOR__ = 'Mikhail Fedosov (tbs.micle@gmail.com)'

from scrapy.item import Item, Field

class ClothesItem(Item):
	title = Field()
	price = Field()
	breadcrumbs = Field()
	image_urls = Field()
	images = Field()

