# -*- coding: utf-8 -*-

import redis

import captureutil
import redis_util

'''
任务分发从redis

逻辑:在redis中新建一个hash表,数据格式如,    100000,no

然后从中一直取数据,取出则把任务标识(初始(0),取出(1),成功(2),失败(3))

'''


# 取出任务
def get_task(redic_client, hash_key, value_key):
    redis_resp = redic_client.hget(hash_key, value_key)
    if redis_resp:
        # 取出任务,并把任务状态置为 'yes'
        redic_client.hset(hash_key, value_key, 1)
    return redis_resp


# 标记任务  任务标识(初始(0),取出(1),成功(2),失败(3))
def sign_task(redic_client, hash_key, value_key, status):
    redic_client.hset(hash_key, value_key, status)


# 得到任务总数,返回是int类型
def get_all_task_size(redis_client, hash_key):
    return redis_client.hlen(hash_key)


# 分发任务界线数量
# def dispatch_task_size(all_task_size, thread_num):
#     sign_task_num = all_task_size / thread_num
#     task_list = []
#     count = 0
#     for index in range(thread_num):
#         count += 1
#         t = (count, int(sign_task_num * count))
#         task_list.append(t)
#     return task_list


#
def get_all_task_iter(redis_client, hash_key):
    result_iter = redis_client.hscan_iter(hash_key)
    return result_iter


# 将任务装入队列
def get_task_queue(queue, task_iter):
    for task in task_iter:
        status = task[1]
        status = captureutil.byte_to_str(status)
        # print("status:", status)
        if status == '0':
            queue.put(task)


if __name__ == '__main__':
    # redisPool = RedisPool()
    # conn = redisPool.connection()
    # redis_client = redis.Redis(connection_pool=redisPool.connection())

    redis_pool = redis_util.get_redis_pool_connection()
    redis_client = redis.Redis(connection_pool=redis_pool)

    # resp = redis_client.hget('jd_20161024', '1000004')
    # resp = resp.decode()
    # print(resp)
    #
    # redis_client.hset('jd_20161024', '1000004', 'yes')
    #
    # print(type(resp))

    # resp = get_task(redis_client, 'jd_20161024', '1000007')
    # print(resp)

    # sign_task(redis_client, 'jd_20161024', '1000007', 7)

    # resp2 = get_all_task_size(redis_client, 'jd_20161024')
    # print(type(resp2))
    # print(resp2)

    # tasks = dispatch_task_size(100, 6)
    #
    # for task in tasks:
    #     print(task)
    #     print(type(task))


    # res = redis_client.hscan_iter("jd_20161024", count=10)
    #
    # print(len(res))

    # first = True
    # for re in res:
    #     print(re)
    #     if first:
    #         print(type(re))
    #         print("----\n")
    #         first = False
    # break


    # res = redis_client.hscan("jd_20161024", 0, None)

    # for r in res:
    #     print(r)






    # cursor, data = redis_client.hscan("jd_20161024", 0, None)

    # print(cursor)
    # print(len(data))
    #
    # cursor, data = redis_client.hscan("jd_20161024", cursor, None)
    #
    # print(cursor)
    # print(len(data))
    # cursor, data = redis_client.hscan("jd_20161024", cursor, None)
    #
    # print(cursor)
    # print(len(data))
    # cursor, data = redis_client.hscan("jd_20161024", cursor, None)
    #
    # print(cursor)
    # print(len(data))

    # print(len(t))


    # for r in t:
    #     print(r)



    res = redis_client.hscan_iter("jd_20161024", None, 10)

    # print(res.__next__())

    for r in res:
        print(r)

    pass
