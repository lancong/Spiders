# -*- coding: utf-8 -*-

import threading
from asyncio import tasks
from queue import Queue

import redis

import fetch_util
import redis_util
import task_dispatch

from jd import jdutil
from time import time
from jd import jdconfig
from jd.jdpage import JDPage

'''

京东爬虫任务开始入口
'''


def jdholder2(task, JDBase, succeedlog, failedlog, outlog, cookie=None, start=10, end=40):
    if cookie:
        JDBase.set_cookie(cookie)
    JDBase.set_succeed_log_path(succeedlog)
    JDBase.set_failed_log_path(failedlog)
    JDBase.set_result_save_path(outlog)
    JDBase.set_useragent(fetch_util.get_pc_useragent())
    JDBase.set_request_path(task)
    JDBase.execute()

    fetch_util.print_log('process  ' + JDBase.getshowlog() + '\t\n')

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


def main():
    # 开始时间
    starttime = time()

    # 日志输出目录
    dirpath = jdconfig.jd_out_dir

    fetch_util.mkdirs(dirpath)

    # 输出结果文件
    outlog = dirpath + jdconfig.jd_out

    redis_pool = redis_util.get_redis_pool_connection()
    redis_client = redis.Redis(connection_pool=redis_pool)

    # all_task_size = task_dispatch.get_all_task_size(redis_client, 'jd_20161024')

    task_iter = task_dispatch.get_all_task_iter(redis_client, 'jd_20161024')

    queue = Queue()

    task_dispatch.get_task_queue(queue, task_iter)

    task_size = queue.qsize()

    if task_size == 0:
        fetch_util.print_log("任务总数为0,结束任务")
        return

    fetch_util.print_log("任务总数: " + str(task_size))

    # 设置cookie
    cookie = jdutil.jd_pc_cookie('beijing')

    jd = JDPage()

    while True:

        threads = []
        for i in range(jdconfig.thread_num):
            # th = threading.Thread(target=jdutil.jdholder, args=(task, jd, succeedlog, failedlog, outlog, cookie, 0, 5))
            th = threading.Thread(target=jdutil.jdholder2, args=(queue, redis_client, jd, outlog, cookie, 5, 10))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

    # 结束时间
    endtime = time()

    fetch_util.print_log("网页数据获取结束,耗时: " + str(float(endtime - starttime) / 60) + "分钟")

    # 写入耗时结果
    costtimepath = dirpath + 'jd_' + fetch_util.get_time_yyyymmddhhmmss() + '.txt'
    fetch_util.write(str(float(endtime - starttime) / 60), costtimepath, 'w')

    pass


if __name__ == '__main__':
    main()

    # ua.update()

    # # 日志输出目录
    # dirpath = jdconfig.jd_out_dir
    # # 输出结果文件
    # outlog = dirpath + jdconfig.jd_out
    # # target urls
    # urlfile = jdconfig.jd_urls
    # # succeed log
    # succeedlog = dirpath + jdconfig.jd_succeed
    # # failed log
    # failedlog = dirpath + jdconfig.jd_failed
    # # 初始化任务
    # # tasks = jdutil.inittask(urlfile, succeedlog, failedlog)
    # # 按thread num 分配任务
    # # tasks = captureutil.dispatchtask(tasks, jdconfig.thread_num)
    # # 设置cookie
    # cookie = jdutil.jd_pc_cookie('beijing')
    # jd = JDPage()


    # tasks = ['3369090']
    # jdutil.jdholder(tasks, jd, succeedlog, failedlog, outlog, cookie)


    # jdutil.jdholder(tasks[0], jd, succeedlog, failedlog, outlog, cookie)


    # list1=[]
    #
    # list1.append("lan1")
    # list1.append("lan2")
    # list1.append("lan3")
    #
    # list2 =[]
    #
    # list2.append(list1)

    # for l in list2:
    #     print(l)
    # print(list2)
    #
    # print(cookie)
    #
    # content = captureutil.urlrequest('http://item.jd.hk/3300092.html', None, cookie, captureutil.getpcua())
    #
    # content = captureutil.htmlformat(content)
    #
    # print(content)



    pass
