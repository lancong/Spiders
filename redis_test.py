# -*- coding: utf-8 -*-

import redis


if __name__ == '__main__':


    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_client = redis.Redis(connection_pool=pool)
    user_name = redis_client.get('user')
    print(user_name)
    print(type(user_name))


    redis_client.set('user','lann')
    user_name = redis_client.get('user')
    print(user_name)
    pass