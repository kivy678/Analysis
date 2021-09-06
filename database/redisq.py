# -*- coding:utf-8 -*-

##########################################################################

import redis
from util.Logger import LOG

##########################################################################


class RedisQueue:
    def __init__(self):
        self._conn = None
        self._conn_pool = None

    def __del__(self):
        if self._conn:
            self.close()

    def connect(self, config):
        if self._conn is None:
            try:
                _conn_pool = redis.ConnectionPool(**config)
                self._conn = redis.StrictRedis(connection_pool=_conn_pool)

                if self._conn.ping() is False:
                    return False

            except Exception as e:
                LOG.info(e)
                return False

        return self._conn

    def close(self):
        self._conn.connection_pool.disconnect()
