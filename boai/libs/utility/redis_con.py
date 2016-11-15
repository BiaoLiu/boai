# coding: utf-8

import redis


class RedisConn:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='120.27.46.167', password='lbican287536', port='6379', db=0)
        self.instance = redis.Redis(connection_pool=self.pool)


redis = RedisConn().instance
