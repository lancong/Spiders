# -*- coding: utf-8 -*-

import redis

import fetch_config


# 得到redis连接池
def get_redis_pool_connection(host=fetch_config.redis_host, port=fetch_config.redis_port):
    pool = redis.ConnectionPool(host=host, port=port)
    return pool


def get_redis_client(pool=get_redis_pool_connection()):
    redis_client = redis.Redis(connection_pool=pool)
    return redis_client
