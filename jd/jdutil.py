# -*- coding: utf-8 -*-

import os
import captureutil
import json

# 适用于聚美
from jd import jdconfig


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


# 适用于聚美
def inittask2(urls, succeedfile, failedfile):
    alltaskreadlines = urls

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

    if succeedfileopener:
        succeedfileopener.close()
    if failedfileopener:
        failedfileopener.close()

    return nowtasks


# def createtask(startid=1, endid=2, allid=4):
# def createtask(startid=188078, total=2, allid=4000000):
def createtask(startid=jdconfig.jd_url_start, total=5000, allid=jdconfig.jd_url_end):
    tasklist = []
    lastid = startid
    for taskid in range(total):
        tempid = startid + taskid
        if tempid <= allid:
            lastid = tempid
            tasklist.append(str(lastid))
            # print("id:" + str(taskid))
    return (tasklist, lastid + 1)


def jd_pc_parameter_dic(areaen):
    parameter_dic = {}
    if areaen == None:
        return parameter_dic
    if areaen.lower() == 'beijing':  # 北京朝阳区
        # 181809404.1907946185.1474426677.1474450676.1474463181.6
        parameter_dic["__jda"] = '181809404.1907946185.1474426677.1474450676.1474463181.6'
        # parameter_dic["__jdb"] = '181809404.2.1907946185|1.1474426677'
        parameter_dic["__jdc"] = '181809404'
        parameter_dic["__jdv"] = '181809404|direct|-|none|-'
        parameter_dic["areaId"] = '1'
        parameter_dic["ipLoc-djd"] = '1-72-4137-0'
        parameter_dic["ipLocation"] = '%u5317%u4EAC'
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
def jd_pc_cookie(areaen):
    cookies = ''
    paramdic = jd_pc_parameter_dic(areaen)
    first = True
    for key in paramdic:
        if first:
            first = False
        else:
            cookies += ';'
        cookies += '{k}={v}'.format(k=key, v=paramdic[key])
    return cookies


# 商品价格
def jd_price(storeid):
    baseurl = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(storeid) + ',J_&type=1'
    priceJson = captureutil.openurl(baseurl)
    if priceJson:
        # [{"id":"J_882282","p":"38.00","m":"45.00","op":"42.00"}]
        js = json.loads(priceJson)
        # 得到一个数组
        js = js[0]
        if 'p' in js:
            return js['p']
    return None


def jdholder(tasks, JDBase, succeedlog, failedlog, outlog, cookie=None, start=10, end=40):
    jd = JDBase

    # if cookie:
    jd.setcookie(cookie)
    jd.setsucceedlog(succeedlog)
    jd.setfailedlog(failedlog)
    jd.setoutputlog(outlog)

    taskslen = len(tasks)

    count = 0

    for task in tasks:
        count += 1

        jd.setua(captureutil.getpcua())
        jd.setrequestpath(task)
        jd.execute()

        captureutil.printlog('process [' + str(count) + '/' + str(taskslen) + '] ' + ' ' + jd.getshowlog() + '\t\n')

        # 获取结果是否成功
        issucceed = jd.getresult()

        if issucceed:
            # 保存成功flag
            jd.savesucceedlog(task)
        else:
            # 保存失败flag
            jd.savefailedlog(task)

        # 睡眠
        jd.sleep(start, end)


if __name__ == '__main__':
    # print(jd_pc_cookie('beijing'))


    price = jd_price("882282")

    print(price)

    # list = createtask()
    #
    # list = createtask(list[1])
    #
    # for l in list[0]:
    #     print("ss   " + l)

    pass
