#!/usr/bin/env python
# -- coding: utf-8 --
from logger import moonbbs_log
from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles
import sqlalchemy
from sqlalchemy import func as sa_func
from sqlalchemy import or_
import sqlalchemy.orm as sa_orm

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
            self.f = open(filename, 'ra+')
        except Exception as e:
            LOG.error('failed to open the file')
            raise e

    def get_keyword_list(self):
        keywords = []
        LOG.info('getting the keyword list')
        for line in self.f:
            keywords.append(line.rstrip())

        keywords = list(set(keywords))
        print(keywords)
        return keywords

    def write_wish(self, wishes):
        wishes_already = self.get_keyword_list()
        try:
            for wish in wishes:
                if (wish not in wishes_already):
                    self.f.write(wish)
                    self.f.write('\n')
                    wishes_already.append(wish)
        except Exception as e:
            LOG.error('cannot write in file')
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
