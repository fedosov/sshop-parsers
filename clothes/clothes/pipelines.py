# -*- coding: utf-8 -*-
__AUTHOR__ = 'Mikhail Fedosov (tbs.micle@gmail.com)'

import os
import shutil
import hashlib
from PIL import Image
from scrapy import log
from cStringIO import StringIO
from settings import IMAGES_STORE
from scrapy.contrib.pipeline.images import ImagesPipeline, ImageException

dir_mined = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mined"))

class ClothesPipeline(object):
	def process_item(self, item, spider):
		subpath = os.path.sep.join(item['breadcrumbs'].split(" > ")[:2])
		path = os.path.join(dir_mined, subpath, item['price'])
		try:
			os.makedirs(path)
		except OSError:
			# path already exists
			pass
		for i, image in enumerate(item['images']):
			shutil.copyfile(os.path.join(IMAGES_STORE, image['path']), os.path.join(path, "%s-%04i%s" % (item['title'], i, os.path.splitext(image['path'])[1])))
		return item

class ClothesImagesPipeline(ImagesPipeline):
	def convert_image(self, image, size=None):
		buf = StringIO()
		try:
			image.save(buf, image.format)
		except Exception, ex:
			raise ImageException("Cannot process image. Error: %s" % ex)
		return image, buf

	def image_key(self, url):
		image_guid = hashlib.sha1(url).hexdigest()
		ext = "jpg" if "Zoom" in url else "png"
		image_key = 'full/%s.%s' % (image_guid, ext)
		return image_key

	def image_downloaded(self, response, request, info):
		try:
			super(ClothesImagesPipeline, self).image_downloaded(response, request, info)
		except IOError, ex:
			log.msg(str(ex), level=log.WARNING, spider=info.spider)