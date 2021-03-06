#!/usr/bin/env python
# -- coding: utf-8 --
from logger import moonbbs_log
from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles
import sqlalchemy
from sqlalchemy import func as sa_func
from sqlalchemy import or_
import sqlalchemy.orm as sa_orm
from jtSDK.jtClient import client
from jtSDK import jtException

import sys

reload(sys)
sys.setdefaultencoding('utf8')

LOG = moonbbs_log()

def _create_engine(connection, **engine_args):
    LOG.debug('sql connection start')

    engine = sqlalchemy.create_engine(connection, **engine_args)

    engine.connect = wrap_db_error(engine.connect)

    return engine

class text_repo(object):

    def __init__(self, filename=None):
        LOG.info('opening file %s'%filename)
        try:
            self.filename = filename
        except Exception as e:
            LOG.error('failed to open the file')
            raise e

    def get_keyword_list(self):
        keywords = []
        LOG.info('getting the keyword list')
        self.r = open(self.filename, 'r')

        for line in self.r:
            LOG.info("get line {0}".format(line))
            keywords.append(line.rstrip())

        keywords = list(set(keywords))
        print(keywords)
        return keywords

    def write_wish(self, wishes):
        wishes_already = self.get_keyword_list()
        self.f = open(self.filename, 'a+')
        try:
            for wish in wishes:
                if (wish not in wishes_already):
                    self.f.write(wish)
                    print(wish)
                    self.f.write('\n')
                    wishes_already.append(wish)
        except Exception as e:
            LOG.error('cannot write in file because of {0}'.format(e))
            raise e
        finally:
            self.f.flush()

class postgres_repo(object):

    def __init__(self, url):
        self.conn_url = url

        engine_args = {
            'pool_recycle': 250,
            'echo': False,
            'convert_unicode': True
        }

        db_conn = None

        try:
            engine = _create_engine(self.conn_url, **engine_args)
            db_conn = engine.connect()
        except Exception as e:
            msg = "Error configuring registry db with supplied sql_connection"
            LOG.error(msg)
            raise e
        finally:
            if db_conn:
                db_conn.close()

        return engine

class jt_repo(object):

    def __init__(self, host = "http://localhost", port = "80", seed_index = 2000):
        self.seed = seed_index
        try:
            self.client = client(host, port)
        except jtException as e:
            LOG.info("unable to connect to json tore because of {0}".format(e))
            raise e

        if (self.client.check_if_index_exist(self.seed)):
            pass
        else:
            try:
                wishes = []
                data = {"wishes": wishes}
                self.client.create_index(self.seed, data)
            except jtException as e:
                LOG.info("unable to create index in json tore because of {0}".format(e))
                raise e

    def get_keyword_list(self):
        # get all indices and process
        try:
            data = self.client.get_index(self.seed)
        except jtException as e:
            LOG.info("unable to get index tore because of {0}".format(e))
            return []
        return data.get("wishes")

    def write_wish(self, wishes):
        # create index
        try:
            data = {"wishes": wishes}
            self.client.update_index(self.seed, data)
        except jtException as e:
            LOG.info("unable to update index tore because of {0}".format(e))
            raise # -*- coding: utf-8 -*-
        return True
