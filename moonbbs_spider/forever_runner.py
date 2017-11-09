#!/usr/bin/env python
# -- coding: utf-8 --
import time
from logger import moonbbs_log

LOG = moonbbs_log()

class runner(object):

    def __init__(self, interval):
        self.interval = interval
        LOG.info('interval time setted as %d'%self.interval)

    def on_start(self, callback, *args, **kwarg):
        while (1):
            try:
                callback(*args)
                time.sleep(self.interval)
            except Exception as e:
                LOG.error('runner is tired of running, jump out!')
                raise e
