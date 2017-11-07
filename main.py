#!/usr/bin/env python
# -- coding: utf-8 --
from forever_runner import runner
from spider import crawler
from repository import text_repo
from notification import email_Notification

from logger import moonbbs_log

LOG = moonbbs_log()

def main():
	moonbbs_runner = runner(5)
	web_spider = crawler()
	reader = text_repo('./wishlist.txt')
	kw = reader.get_keyword_list()
        email_server = email_Notification('loveyouforever36@gmail.com', '*********')
	moonbbs_runner.on_start(web_spider.crawl, kw, email_server)


if __name__ == "__main__": main()
