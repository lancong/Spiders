# -*- coding:utf-8 -*-

import threading

from jd2 import jd_parser


class WorkManager(object):
    def __init__(self, queue, redis_client, cookie=None, host=None, path=None, thread_num=2):
        self.work_queue = queue
        self.threads = []
        # self.__init_work_queue(work_num)

        self.redis_client = redis_client
        self.cookie = cookie
        self.host = host
        self.path = path
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue, self.redis_client, self.cookie, self.host, self.path))

    """
        初始化工作队列
    """

    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    """
        添加一项工作入队
    """

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))  # 任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive(): item.join()


class Work(threading.Thread):
    def __init__(self, work_queue, redis_client, cookie=None, host=None, path=None):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.redis_client = redis_client
        self.cookie = cookie
        self.host = host
        self.path = path
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                task_id, task_sign = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                # do(args)
                do_job(task_id, self.redis_client, self.cookie, self.host, self.path)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break


# 具体要做的任务
def do_job(task_id, redis_client, cookie=None, host=None, path=None):
    # time.sleep(0.1)  # 模拟处理时间
    # print(threading.current_thread(), list(args))

    jd_parser.jd_spider_task(task_id, redis_client, cookie, host, path)
