#!/usr/bin/env python
# -- coding: utf-8 --
from forever_runner import runner
from spider import crawler
from repository import text_repo
from notification import email_Notification

from logger import moonbbs_log

LOG = moonbbs_log()

class main_service(object):

    def __init__(self, reader = None):
        self.interval = 5
        self.reader = reader
        self.email_server = None

    def set_interval(self, interval):
        self.interval = interval

    def set_email(self, email, password):
        try:
            self.email_server = email_Notification(email, password)
        except Exception as e:
            LOG.error("failed to set up email for user")
            raise e

    def on_start(self):
        if (self.reader == None or self.email_server == None):
            LOG.error("user failed to put in all info, exiting")
            raise Exception('missing info')
        if (len(reader.get_keyword_list()) == 0):
            LOG.error("no wishes added")
            raise Exception('missing wishes')
    	self.moonbbs_runner = runner(self.interval)
    	self.web_spider = crawler()
    	kw = self.reader.get_keyword_list()
    	self.moonbbs_runner.on_start(self.web_spider.crawl, kw, self.email_server)
