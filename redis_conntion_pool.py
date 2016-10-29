# -*- coding: utf-8 -*-
from time import time

import redis

import captureconfig
import captureutil

'''
redis conntion pool
'''


class RedisPool(object):
    def __init__(self, host=captureconfig.redis_host, port=captureconfig.redis_port):
        self.host = host
        self.port = port

    def connection(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port)
        return pool


class GlobalRedisPool(object):
    """ThreadPool Singleton class."""

    _instance = None

    def __init__(self):
        """Create singleton instance """

        if GlobalRedisPool._instance is None:
            # Create and remember instance
            GlobalRedisPool._instance = RedisPool()

    def __getattr__(self, attr):
        """ Delegate get access to implementation """
        return getattr(self._instance, attr)

    def __setattr__(self, attr, val):
        """ Delegate set access to implementation """
        return setattr(self._instance, attr, val)


if __name__ == '__main__':
    # pool = RedisPool(GlobalRedisPool)
    # pool = GlobalRedisPool.__init__()
    # connection = GlobalRedisPool.__getattr__(RedisPool.__base__,'connection')


    redisPool = RedisPool()
    conn = redisPool.connection()
    redis_client = redis.Redis(connection_pool=redisPool.connection())

    # redis_client.append('user', ' lan')
    # user = redis_client.get('user')
    # user = user.decode()
    # print(user)

    # conn = GlobalRedisPool.__getattr__(RedisPool,'connection')
    # r = redis.Redis(connection_pool=conn)
    # user = r.get('user')
    # print(user)


    # -----------

    start = time()

    for l in range(1000100, 1000150):
        redis_client.hset("jd_20161024", l, "0")

    # redis_client.hset("jd_20161024", '100', "0")
    # lss = []
    # for l in range(1000):
    #     redis_client.sadd('all_task', l)

    # redis_client.sadd('all_task', set(lss))
    # redis_client.sadd('succeed_task', set(lss))

    # -----------
    end = time()

    print(end - start)

    # res = redis_client.smembers('all_task')


    # redis_client.sdiffstore('new_task','all_task','succeed_task')


    # ----------

    # redis_client.sadd('all_task', "aa", 'fsd', "bb", "cc")
    # redis_client.sadd('succeed_task', "bb", "cc")
    # redis_client.sadd('succeed_task2', "dd", "cc")
    # redis_client.sadd('succeed_task3', "ee", "ff")
    # redis_client.sadd('new_task', "bb", "cc", "dd")
    #
    # captureutil.print_log_debug(redis_client.sdiff('all_task', 'succeed_task', 'succeed_task2', 'succeed_task3'))
    # redis_client.sdiffstore('new_task', 'all_task', 'succeed_task')

    # ----------

    # captureutil.print_log_debug(redis_client.sdiff('new_task','all_task', 'succeed_task'))

    # redis_client.sinterstore('new_task2','all_task','succeed_task')
    # redis_client.sunionstore('new_task3','all_task','succeed_task')


    #
    # redis_client.delete('all_task')
    # redis_client.delete('new_task')
    # redis_client.delete('new_task2')
    # redis_client.delete('new_task3')
    # redis_client.delete('succeed_task')
    # redis_client.delete('succeed_task2')
    # redis_client.delete('succeed_task3')

    # print(res)
    # print(type(res))


    # -----------------

    # alllss = redis_client.sscan_iter('all_task',None,5)
    #
    # print(type(alllss))
    #
    # while True:
    #     try:
    #         ls = alllss.__next__()
    #         print("ls: ",ls)
    #         print(type(ls))
    #         print('------------\n')
    #         break
    #
    #     except:
    #         break

    # -----------------



    # redis_client.srem('all_task','544','44')

    # captureutil.print_log_debug(redis_client.srem('all_task','22'))


    # 2016.10.28 15:45:49 [b'941', b'517', b'672', b'145', b'985']
    # ts = redis_client.srandmember('all_task', 5)
    # captureutil.print_log_debug(type(ts))
    # captureutil.print_log_debug(ts)

    # lr=[]
    # for t in ts:
    #     lr.append(t.decode())
    #
    # print(len(lr))
    #
    # redis_client.srem('all_tasks', lr)

    # captureutil.print_log_debug(redis_client.spop('all_task'))



    # captureutil.print_log_debug(redis_client.scard('all_task'))


    # l = ['1000001', '1000002', '1000003']
    # ls = redis_client.hmget("jd_20161024", "1000000", "1000001", "1000002")
    #
    # print(ls)

    pass
