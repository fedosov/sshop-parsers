# -*- coding: utf-8 -*-
__AUTHOR__ = 'Mikhail Fedosov (tbs.micle@gmail.com)'

import csv
import random

cr = csv.reader(open("user_agents.csv", "rb"))
ua_list = [row[1] for row in cr]

class RandomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		ua  = random.choice(ua_list)
		if ua:
			request.headers.setdefault('User-Agent', ua)