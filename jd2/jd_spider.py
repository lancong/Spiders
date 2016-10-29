# -*- coding: utf-8 -*-

import redis
import threading
import redis_util
import fetch_util
import task_dispatch

from queue import Queue

from jd2 import jd_config
from jd2 import jd_parser
from jd2 import jd_util




# 程序入口
def main():
    redis_pool = redis_util.get_redis_pool_connection()
    redis_client = redis.Redis(connection_pool=redis_pool)

    task_iter = task_dispatch.get_all_task_iter(redis_client, jd_parser.redis_task_key)
    # 任务队列
    queue = Queue()
    # 更新任务队列内容
    task_dispatch.get_task_queue(queue, task_iter)

    # 可执行任务总数
    task_size = queue.qsize()
    fetch_util.print_log_debug("任务总数为:" + str(task_size))

    # cookie
    cookie = jd_util.jd_pc_cookie('beijing')
    # request header host:host
    host = 'item.jd.hk'
    # result save path

    # 结果保存路径
    path = jd_config.result_save_path

    # jd_parser.task(queue, redis_client, cookie, host, path)

    threads = []

    for i in range(10):
        th = threading.Thread(target=jd_parser.task, args=(queue, redis_client, cookie, host, path))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    fetch_util.print_log_debug("finish")

if __name__ == '__main__':
    main()

    pass
