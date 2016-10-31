# -*- coding: utf-8 -*-

import redis
import threading
import redis_util
import fetch_util
import task_dispatch

from time import time
from jd2 import jd_util
from queue import Queue
from jd2 import jd_queue
from jd2 import jd_config
from jd2 import jd_parser

# 程序入口
from jd2.jd_queue import WorkManager


def main():
    redis_pool = redis_util.get_redis_pool_connection()
    redis_client = redis.Redis(connection_pool=redis_pool)

    task_iter = task_dispatch.get_all_task_iter(redis_client, jd_config.redis_task_key)

    # 任务队列
    queue = Queue()
    # 将数据加入队列
    task_dispatch.get_task_queue(queue, task_iter)

    # 可执行任务总数
    task_size = queue.qsize()
    fetch_util.print_log_debug("可执行任务总数为:" + str(task_size))

    # cookie
    cookie = jd_util.jd_pc_cookie('beijing')

    # request header host:host
    host = 'item.jd.hk'

    # 结果保存路径
    path = jd_config.result_save_path

    # jd_parser.task(queue, redis_client, cookie, host, path)

    threads = []

    for i in range(jd_config.thread_num):
        th = threading.Thread(target=jd_parser.task, args=(queue, redis_client, cookie, host, path))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    fetch_util.print_log_debug("finish")


def out_exec_result(cost_time, redis_client):
    pass


# 程序入口
def main2():
    # 开始时间
    start_time = time()
    start_time_detail = fetch_util.get_time_yyyymmddhhmmss2()

    redis_pool = redis_util.get_redis_pool_connection()
    redis_client = redis.Redis(connection_pool=redis_pool)

    task_iter = task_dispatch.get_all_task_iter(redis_client, jd_config.redis_task_key)
    # 任务队列
    queue = Queue()
    # 更新任务队列内容
    task_dispatch.get_task_queue(queue, task_iter)

    # 可执行任务总数
    task_size = queue.qsize()
    fetch_util.print_log_debug("任务总数为:" + str(task_size))

    # cookie
    cookie = jd_util.jd_pc_cookie('beijing')
    # get 请求中的header, request header host:host
    host = 'item.jd.hk'

    # 结果保存路径
    path = jd_config.result_save_path

    # 任务管理器
    work_manager = WorkManager(queue, redis_client, cookie, host, path, jd_config.thread_num)
    work_manager.wait_allcomplete()
    # 结束时间
    end_time = time()
    end_time_detail = fetch_util.get_time_yyyymmddhhmmss2()

    # 到此任务已经结束
    # fetch_util.print_log_debug("task finished")

    # ------------- 后面是统计日志

    # 耗时
    cost_time = (float(end_time - start_time) / 60)

    save_result_log(cost_time, end_time_detail, redis_client, start_time_detail, task_size)

    # --------------------------


# 任务结果日志
def save_result_log(cost_time, end_time_detail, redis_client, start_time_detail, task_size):
    # 任务成功计数
    task_succeed_count = redis_client.get(jd_config.redis_succeed_count_key)
    task_succeed_count = fetch_util.byte_to_str(task_succeed_count)
    if not task_succeed_count:
        task_succeed_count = '0'
    # 任务失败计数
    task_faileed_count = redis_client.get(jd_config.redis_failed_count_key)
    task_faileed_count = fetch_util.byte_to_str(task_faileed_count)
    if not task_faileed_count:
        task_faileed_count = '0'
    fetch_util.print_log_debug("成功: " + task_succeed_count)
    fetch_util.print_log_debug("失败: " + task_faileed_count)
    result_log = '开始时间:\t' + start_time_detail + '\n\n' + '结束时间:\t' + end_time_detail + '\n\n'
    result_log += '任务总数:\t' + str(task_size) + '\n\n' + '成功总数:\t' + str(
            task_succeed_count) + '\n\n' + '失败总数:\t' + str(task_faileed_count) + '\n\n' + '耗时\t' + str(
            cost_time) + 'm'
    fetch_util.write(result_log, jd_config.log_save_path, 'w')


if __name__ == '__main__':
    main2()

    pass
