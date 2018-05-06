#!/usr/bin/env python
# -- coding: utf-8 --
from bs4 import BeautifulSoup
import requests
import urllib2
from logger import moonbbs_log
from pprint import pprint
from notification import msg_queue, email_Notification
import sys

reload(sys)
sys.setdefaultencoding('utf8')

LOG = moonbbs_log()

class crawler(object):

	def __init__(self):
		LOG.debug('setting the url to http://www.moonbbs.com/forum-46-1.html, \
					which is manually set. Can be improved')
		self.url = 'http://www.moonbbs.com/forum-46-1.html'
		self.notification_tunnel = msg_queue()

	def crawl(self, keyword=None, email_server=None):
		LOG.info('start crawling')
		print('Crawling start!')
		print(len(keyword))
		response = urllib2.urlopen(self.url)
		web = response.read()

		soup = BeautifulSoup(web, 'html.parser')

		links = soup.findAll('a', {'class': 'xst'})

		lists = {}
		keywords = []

		for link in links:
			lists[link.text] = link.get('href')
			keywords.append(link.text)

			for words in keyword:
				print str(words)
				if words in str(link.text):
					msg = ('Item: %s, Url: %s' % (link.text, link.get('href')))
					print msg
					self.notification_tunnel.enqueue(msg)
					print(self.notification_tunnel.size_of_unsent())

		print('Crawling finished!')
		LOG.info('stop crawling, and start to flushing')
		self.notification_tunnel.flush(email_server)
		return lists, keywords
