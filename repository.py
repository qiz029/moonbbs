#!/usr/bin/env python
# -- coding: utf-8 --
from logger import moonbbs_log

LOG = moonbbs_log()

class text_repo(object):

    def __init__(self, filename=None):
        LOG.info('opening file %s'%filename)
        try:
            self.f = open(filename, 'r')
        except Exception as e:
            LOG.error('failed to open the file')
            raise e

    def get_keyword_list(self):
        keywords = []
        LOG.info('getting the keyword list')
        for line in self.f:
            keywords.append(line.rstrip())

        return keywords
