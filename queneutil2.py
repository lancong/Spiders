# !/usr/bin/env python
# -*- coding:utf-8 -*-  

from queue import Queue
import threading
import time

import captureutil
from jd import jdutil


class WorkManager(object):
    def __init__(self, work_num=1000, thread_num=2):
        self.work_queue = Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    """ 
        初始化线程 
    """

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

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
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break

def jdholder(task, JDBase, succeedlog, failedlog, outlog, cookie=None, start=10, end=40):
    if cookie:
        JDBase.set_cookie(cookie)

    JDBase.set_succeed_log_path(succeedlog)
    JDBase.set_failed_log_path(failedlog)
    JDBase.set_result_save_path(outlog)
    JDBase.set_useragent(captureutil.get_pc_useragent())
    JDBase.set_request_path(task)
    JDBase.execute()

    captureutil.print_log('process  ' + JDBase.getshowlog() + '\t\n')

    # 获取结果是否成功
    issucceed = JDBase.get_result()

    if issucceed:
        # 保存成功flag
        JDBase.save_succeed_log(task)
    else:
        # 保存失败flag
        JDBase.save_failed_log(task)

        # 睡眠
    JDBase.sleep(start, end)


# 具体要做的任务
def do_job(*args):
    # time.sleep(0.1)  # 模拟处理时间
    # print(threading.current_thread(), list(args))
    jdutil.jdholder2(args[0], args[1], args[2], args[3], args[4], args[5])
    pass


if __name__ == '__main__':
    start = time.time()
    work_manager = WorkManager(100, 10)  # 或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    print("cost all time: %s" % (end - start))
