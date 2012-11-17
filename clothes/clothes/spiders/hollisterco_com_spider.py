# -*- coding: utf-8 -*-
__AUTHOR__ = 'Mikhail Fedosov (tbs.micle@gmail.com)'

import re
from clothes.items import ClothesItem
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

PAGE_TYPE_OLD = 0
PAGE_TYPE_UPDATED = 1

class HollistercoComSpider(CrawlSpider):
	name = "hollisterco_com"
	allowed_domains = ["www.hollisterco.com", "eu.hollisterco.com", "us.hollisterco.com", "uk.hollisterco.com"]
	# Example category
	start_urls = [
		#"http://www.hollisterco.com",
		#"http://www.hollisterco.com/webapp/wcs/stores/servlet/CategoryDisplay?catalogId=10201&storeId=11205&langId=-1&topCategoryId=12552&categoryId=109773&parentCategoryId=109773",
	    # TESTING
#		"http://www.hollisterco.com/webapp/wcs/stores/servlet/ProductDisplay?catalogId=10201&storeId=11205&langId=-1&categoryId=108705&parentCategoryId=108705&topCategoryId=12552&productId=1047769&seq=01",
#		"http://www.hollisterco.com/webapp/wcs/stores/servlet/ProductDisplay?catalogId=10201&categoryId=106210&langId=-1&parentCategoryId=106210&productId=1040419&storeId=11205&topCategoryId=",
	    # PRODUCTION URL
		"http://www.hollisterco.com/webapp/wcs/stores/servlet/SiteMapView?storeId=11205&catalogId=10201&langId=-1",
	]
	rules = (
		Rule(SgmlLinkExtractor(allow=('CategoryDisplay', ))),
		Rule(SgmlLinkExtractor(allow=('ProductDisplay', )), callback='parse_item', follow=False),
	)

	def __init__(self, *a, **kw):
		super(HollistercoComSpider, self).__init__(*a, **kw)
		self.visited_items = set()

	def parse_item(self, response):
		print response.url
		hxs = HtmlXPathSelector(response)

		product_page_type = PAGE_TYPE_OLD
		products = hxs.select('//div[@class="product "]')
		if not products:
			product_page_type = PAGE_TYPE_UPDATED
			products = hxs.select('//div[@class="product updated-product-page  "]')
		for product in products:
			data_form = product.select('.//div[@class="vertical-positioner"]/div[@class="product-form"]//form[@id="product-add-to-bag"]')
			item = ClothesItem()
			item['title'] = "".join(data_form.select('.//input[@name="name"]/@value').extract())
			item['price'] = ("".join(data_form.select('.//input[@name="price"]/@value').extract())).replace("&nbsp;", " ")
			item['price'] = item['price'].replace("&euro;", "EURO")
			item['price'] = item['price'].replace("&pound;", "POUND")
			item['breadcrumbs'] = "".join(data_form.select('.//input[@name="comment"]/@value').extract())
			item['images'] = []
			item['image_urls'] = []
			item_unique_string = "%s--%s--%s" % (item['title'], item['price'], item['breadcrumbs'])
			if item_unique_string in self.visited_items:
				print "< skip >"
				continue
			self.visited_items.add(item_unique_string)
			print "Title: %s\nPrice: %s\nBC: %s" % (item['title'], item['price'], item['breadcrumbs'])

			# Photos extracting
			base_image_src = "".join(product.select('.//div[contains(@class,"product-view")]//img[@class="prod-img"]/@src').extract())
			if base_image_src:
				images_count = max(1, len(product.select('.//div[@class="vertical-positioner"]/div[@class="product-form"]//div[contains(@class,"swatches")]//a[@class="swatch-link"]')))
				base_image_src = base_image_src.replace("//", "http://")
				print "-" * 50
				for i in xrange(1, images_count + 1):
					image_src_small = re.sub(r"_(\d+)_prod", "_%02d_prod" % i, base_image_src)
					if product_page_type == PAGE_TYPE_OLD:
						image_src_big = "%sS7Zoom$&scl=3.0" % image_src_small[:-1]
					elif product_page_type == PAGE_TYPE_UPDATED:
						#image_src_big = "%sImageMagnify$" % image_src_small[:-1]
						image_src_big = image_src_small.replace("500$", "Magnify$")
					print image_src_big
					item['image_urls'].append(image_src_big)
			else:
				print "NO IMAGES"

			yield item

