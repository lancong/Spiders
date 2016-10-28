# -*- coding: utf-8 -*-

import threading
import captureutil

from jumei import jumeiconfig
from jumei.jumeiurlstartwithd import JumeiUrlStartWithD
from jumei.jumeiutil import inittask, jumeiholder, jumei_pc_cookie


def main():
    # 日志输出目录
    dirpath = jumeiconfig.jumei_out_dir
    # 输出结果文件
    outlog = dirpath + jumeiconfig.jumei_d_out
    # target urls
    urlfile = jumeiconfig.jumei_d_urls
    # succeed log
    succeedlog = dirpath + jumeiconfig.jumei_d_succeed
    # failed log
    failedlog = dirpath + jumeiconfig.jumei_d_failed
    # 初始化任务
    tasks = inittask(urlfile, succeedlog, failedlog)
    # 按thread num 分配任务
    tasks = captureutil.task_dispatch(tasks, jumeiconfig.thread_num)
    # 设置cookie
    cookie = jumei_pc_cookie('beijing')
    # JumeiUrlStartWithD 实例
    jumei = JumeiUrlStartWithD()

    threads = []

    for task in tasks:
        th = threading.Thread(target=jumeiholder, args=(task, jumei, succeedlog, failedlog, outlog, cookie))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


if __name__ == '__main__':
    main()

    pass
