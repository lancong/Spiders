# -*- coding: utf-8 -*-

import threading
import captureutil

from jd import jdutil
from time import time
from jd import jdconfig
from jd.jdpage import JDPage

'''

京东爬虫任务开始入口
'''

def main():
    # 开始时间
    starttime = time()

    # 日志输出目录
    dirpath = jdconfig.jd_out_dir

    captureutil.mkdirs(dirpath)

    # 输出结果文件
    outlog = dirpath + jdconfig.jd_out
    # target urls
    urlfile = jdconfig.jd_urls

    total = jdconfig.jd_url_end - jdconfig.jd_url_start
    allurls = jdutil.createtask(jdconfig.jd_url_start, total)

    # succeed log
    succeedlog = dirpath + jdconfig.jd_succeed
    # failed log
    failedlog = dirpath + jdconfig.jd_failed
    # 初始化任务
    inittasks = jdutil.init_task2(allurls, succeedlog, failedlog)

    captureutil.print_log("任务总数: " + str(len(inittasks)))

    # 按thread num 分配任务
    tasks = captureutil.task_dispatch(inittasks, jdconfig.thread_num)

    # 设置cookie
    cookie = jdutil.jd_pc_cookie('beijing')

    jd = JDPage()

    while True:

        threads = []
        for task in tasks:
            # th = threading.Thread(target=jdutil.jdholder, args=(task, jd, succeedlog, failedlog, outlog, cookie, 0, 5))
            th = threading.Thread(target=jdutil.jdholder, args=(task, jd, succeedlog, failedlog, outlog, cookie, 5, 10))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

    # 结束时间
    endtime = time()

    captureutil.print_log("网页数据获取结束,耗时: " + str(float(endtime - starttime) / 60) + "分钟")

    # 写入耗时结果
    costtimepath = dirpath + 'jd_' + captureutil.time_format_yyyymmddhhmmss() + '.txt'
    captureutil.write(str(float(endtime - starttime) / 60), costtimepath, 'w')

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
