# -*- coding: utf-8 -*-

import threading
import fetch_util

from jumei import jumeiconfig
from jumei.jumeiurlstartwithh import JumeiUrlStartWithH
from jumei.jumeiutil import inittask, jumeiholder


def main():
    # 日志输出目录
    dirpath = jumeiconfig.jumei_out_dir
    # 输出结果文件
    outlog = dirpath + jumeiconfig.jumei_h_out
    # target urls
    urlfile = jumeiconfig.jumei_h_urls
    # succeed log
    succeedlog = dirpath + jumeiconfig.jumei_h_succeed
    # failed log
    failedlog = dirpath + jumeiconfig.jumei_h_failed
    # 初始化任务
    tasks = inittask(urlfile, succeedlog, failedlog)
    # 按thread num 分配任务
    tasks = fetch_util.task_dispatch(tasks, jumeiconfig.thread_num)

    # JumeiUrlStartWithD 实例
    jumei = JumeiUrlStartWithH()

    threads = []

    for task in tasks:
        th = threading.Thread(target=jumeiholder, args=(task, jumei, succeedlog, failedlog, outlog, None))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


if __name__ == '__main__':
    main()

    pass
