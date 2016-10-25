# -*- coding: utf-8 -*-
import os

import captureutil


# 适用于聚美
def inittask(urlsfile, succeedfile, failedfile):
    exist = captureutil.isfileexist(urlsfile)

    if not exist:
        captureutil.printlog(urlsfile + " not exist")
        return []

    alltaskopener = open(urlsfile, 'r')
    alltaskreadlines = alltaskopener.readlines()

    succeedfileopener = None
    succeedfilereadlines = []
    if os.path.exists(succeedfile):
        succeedfileopener = open(succeedfile, "r")
        succeedfilereadlines = succeedfileopener.readlines()

    failedfileopener = None
    failedfilereadlines = []
    if os.path.exists(failedfile):
        failedfileopener = open(failedfile, "r")
        failedfilereadlines = failedfileopener.readlines()

    beforetasks = captureutil.removeduplicate(succeedfilereadlines, alltaskreadlines)
    nowtasks = captureutil.removeduplicate(failedfilereadlines, beforetasks)

    if alltaskopener:
        alltaskopener.close()
    if succeedfileopener:
        succeedfileopener.close()
    if failedfileopener:
        failedfileopener.close()

    return nowtasks


# 生成cookies
def jumei_pc_parameter_dic(areaen):
    parameter_dic = {}
    if areaen == None:
        return parameter_dic
    if areaen.lower() == 'beijing':  # 北京朝阳区
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22bj%22%2C%22city%22%3A%22beijing%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dbj%26city%3Dbeijing'
    elif areaen.lower() == 'guangzhou':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22gz%22%2C%22city%22%3A%22guangdong%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dgz%26city%3Dguangdong'
    elif areaen.lower() == 'shanghai':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22sh%22%2C%22city%22%3A%22shanghai%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dsh%26city%3Dshanghai'
    elif areaen.lower() == 'chengdu':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22cd%22%2C%22city%22%3A%22sichuan%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dcd%26city%3Dsichuan'
    return parameter_dic


# 取得地区cookies
def jumei_pc_cookie(areaen):
    cookies = ''
    paramdic = jumei_pc_parameter_dic(areaen)
    first = True
    for key in paramdic:
        if first:
            first = False
            pass
        else:
            cookies += ';'
        cookies += '{k}={v}'.format(k=key, v=paramdic[key])
    return cookies


def jumeiholder(tasks, JuMeiBase, succeedlog, failedlog, outlog, cookie=None, start=10, end=40):
    jumei = JuMeiBase

    # if cookie:
    jumei.setcookie(cookie)
    jumei.setsucceedlog(succeedlog)
    jumei.setfailedlog(failedlog)
    jumei.setoutputlog(outlog)

    taskslen = len(tasks)

    count = 0

    for task in tasks:
        count += 1

        jumei.setua(captureutil.getpcua())
        jumei.setrequestpath(task)
        jumei.execute()

        captureutil.printlog('process [' + str(count) + '/' + str(taskslen) + '] ' + ' ' + jumei.getshowlog() + '\t\n')

        # 获取结果是否成功
        issucceed = jumei.getresult()

        if issucceed:
            # 保存成功flag
            jumei.savesucceedlog(task)
        else:
            # 保存失败flag
            jumei.savefailedlog(task)

        # 睡眠
        jumei.sleep(start, end)
