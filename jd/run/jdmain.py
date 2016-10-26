# -*- coding: utf-8 -*-


import os
import threading
from time import time

import captureutil
from jd import jdutil
from jd import jdconfig

# 初始化任务
from jd.jdpage import JDPage


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

    # 最后一次生成任务的id
    lastindexlogpath = dirpath + jdconfig.jd_lastindex

    if os.path.exists(lastindexlogpath):
        with open(lastindexlogpath, 'r') as lasttaskid:
            lasttaskid = int(lasttaskid.readline())
        # ----------- 注意
        total = lasttaskid - jdconfig.jd_url_start
        if total <= 0:
            total = 1000
        allurls = jdutil.createtask(jdconfig.jd_url_start, total)
    else:
        allurls = jdutil.createtask()
        lasttaskid = allurls[1]

    # succeed log
    succeedlog = dirpath + jdconfig.jd_succeed
    # failed log
    failedlog = dirpath + jdconfig.jd_failed
    # 初始化任务
    inittasks = jdutil.inittask2(allurls[0], succeedlog, failedlog)

    captureutil.printlog("任务总数: " + str(len(inittasks)))

    # 按thread num 分配任务
    tasks = captureutil.dispatchtask(inittasks, jdconfig.thread_num)

    # 设置cookie
    cookie = jdutil.jd_pc_cookie('beijing')

    jd = JDPage()

    first = True

    while True:

        if not first:
            allurls = jdutil.createtask(int(lasttaskid))
            lasttaskid = allurls[1]
            # 写入上次任务生成id
            captureutil.write(str(lasttaskid), lastindexlogpath, 'w')
            tasks = captureutil.dispatchtask(allurls[0], jdconfig.thread_num)
            if len(tasks) <= 0:
                break
        else:
            first = False

        threads = []
        for task in tasks:
            # th = threading.Thread(target=jdutil.jdholder, args=(task, jd, succeedlog, failedlog, outlog, cookie, 0, 5))
            th = threading.Thread(target=jdutil.jdholder, args=(task, jd, succeedlog, failedlog, outlog, cookie, 5, 20))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

            # captureutil.printlog("我又完成一次任务")

    # 结束时间
    endtime = time()

    captureutil.printlog("网页数据获取结束,耗时: " + str(float(endtime - starttime) / 60) + "分钟")

    # 写入耗时结果
    costtimepath = dirpath + 'jd_' + captureutil.time_format_yyyymmddhhmmss() + '.txt'
    captureutil.write(str(float(endtime - starttime) / 60), costtimepath, 'w')

    pass


if __name__ == '__main__':
    main()

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
