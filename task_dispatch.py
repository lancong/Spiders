# -*- coding: utf-8 -*-


'''
任务分发从redis

逻辑:在redis中新建一个hash表,数据格式如,    100000,no

然后从中一直取数据,取出则把任务标识(初始(0),取出(1),成功(2),失败(3))

'''

import redis
from redis_conntion_pool import RedisPool


# 取出任务
def get_task(redic_client, task_table, task_key):
    redis_resp = redic_client.hget(task_table, task_key)
    if redis_resp:
        # 取出任务,并把任务状态置为 'yes'
        redic_client.hset(task_table, task_key, 1)
    return redis_resp


# 标记任务  任务标识(初始(0),取出(1),成功(2),失败(3))
def sign_task(redic_client, task_table, task_key, status):
    redic_client.hset(task_table, task_key, status)


if __name__ == '__main__':
    redisPool = RedisPool()
    conn = redisPool.connection()
    redis_client = redis.Redis(connection_pool=redisPool.connection())

    # resp = redis_client.hget('jd_20161024', '1000004')
    # resp = resp.decode()
    # print(resp)
    #
    # redis_client.hset('jd_20161024', '1000004', 'yes')
    #
    # print(type(resp))

    resp = get_task(redis_client, 'jd_20161024', '1000007')
    print(resp)

    sign_task(redis_client, 'jd_20161024', '1000007', 7)

    pass
