# -*- coding: utf-8 -*-
__AUTHOR__ = 'Mikhail Fedosov (tbs.micle@gmail.com)'

import os

BOT_NAME = 'Google'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['clothes.spiders']
NEWSPIDER_MODULE = 'clothes.spiders'

# Settings
COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 40
LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 1,
	'clothes.random_user_agent.RandomUserAgentMiddleware': 2,
	'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 3,
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = [
	'clothes.pipelines.ClothesImagesPipeline',
	'clothes.pipelines.ClothesPipeline',
]

DEFAULT_REQUEST_HEADERS = {
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.3',
}

EXTENSIONS = {
	'scrapy.contrib.closespider.CloseSpider': 500,
}

# DEBUG
#CLOSESPIDER_ITEMCOUNT = 1

IMAGES_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mined_img")
