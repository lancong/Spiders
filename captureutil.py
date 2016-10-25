# -*- coding: utf-8 -*-

import codecs
import gzip
from http import cookiejar
from io import StringIO
import os
import random
import time
import urllib

import requests
from bs4 import BeautifulSoup

import captureconfig
import urllib.request
from urllib.parse import quote


# 网络请求,并返回页面
def urlrequest(url, referurl=None, cookie=None, useragent=None, postdata=None, ip=None, timeout=60):
    cookie_support = urllib.request.HTTPCookieProcessor(cookiejar.CookieJar())
    if ip:
        proxy_support = urllib.request.ProxyHandler({'http': ip})
        opener = urllib.request.build_opener(proxy_support, cookie_support, urllib.request.ProxyBasicAuthHandler())
        urllib.request.install_opener(opener)
    else:
        opener = urllib.request.build_opener(cookie_support, urllib.request.ProxyBasicAuthHandler())
        urllib.request.install_opener(opener)

    headers = {'User-Agent': useragent}

    req = urllib.request.Request(url, headers=headers)

    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml')

    # req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    # req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

    if referurl:
        req.add_header('Referer', referurl)
    if cookie:
        req.add_header('Cookie', cookie)
    if postdata:
        # try:
        #     urllib.parse.urlencode(postdata)
        # except:
        pass

    content = ''

    try:
        # 超时会产生异常
        content = urllib.request.urlopen(req, timeout=timeout).read()
    except:
        pass

    try:
        gzp_content = StringIO(content)
        gzipper = gzip.GzipFile(fileobj=gzp_content)
        content = gzipper.read()
    except:
        1
    return content


def openurl(url):
    session = requests.session()
    headers = {
        "User-Agent": getpcua(),
        "Accept": "text/html,application/xhtml+xml,application/xml"}
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    req = session.get(url, headers=headers)
    req.encoding = "utf-8"
    # return BeautifulSoup(req.text, "html.parser")
    return req.text


# pc user-agent
def getpcua():
    ua = captureconfig.user_agent_pc
    index = randnum(0, len(ua) - 1)
    return ua[index]
    pass


# mobile user-agent
def getmoblieua():
    ua = captureconfig.user_agent_mobile
    index = randnum(0, len(ua) - 1)
    return ua[index]


# 时间格式 20160202
def time_format_yyyymmdd():
    return time.strftime("%Y%m%d", time.localtime(time.time()))


# 时间格式 2016-02-02
def time_format_yyyymmdd2():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


# 时间格式 19:24:25
def time_format_hhmmss():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


# 时间格式 20160202112222
def time_format_yyyymmddhhmmss():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


# 时间格式 2016-02-02 11:22:22
def time_format_yyyymmddhhmmss2():
    return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))


def mkdirs(path):
    path = path.strip()
    path = path.rstrip("/")
    if not os.path.exists(path):
        os.makedirs(path)


def write(data, path, mode="a", charset='utf-8'):
    writer = None
    try:
        writer = codecs.open(path, mode, charset)
        writer.write(data)
        writer.write("\r\n")
        writer.flush()
    except:
        print("write file to " + path + " error")
    finally:
        if writer:
            writer.close()


# 生成随机整形数字
def randnum(minnum, maxnum):
    return random.randint(minnum, maxnum)


# 编码URL中字符
def urlencode(text):
    return quote(str(text))


# 删除文件
def deletefile(file):
    if os.path.exists(file):
        os.remove(file)


# 分发任务
def dispatchtask(lists, threadnum):
    # 单线程不拆分任务
    if threadnum < 1:
        return lists

    # list size
    listsize = len(lists)

    # 任务总列表
    tasklists = []

    if threadnum > listsize:
        tasklists.append(lists)
        return tasklists

    single_task_num = int(listsize / threadnum)

    # 任务容器
    task = []

    count = 0
    taskindex = 0

    for index in range(listsize):
        task.append(lists[index])
        count += 1
        if count == single_task_num and len(tasklists) < threadnum:
            tasklists.append(task)
            task = []
            count = 0
        elif len(tasklists) == threadnum:
            tasklists[taskindex].append(lists[index])
            taskindex += 1

    printlog("thread queue: " + str(len(tasklists)) + '\t\n')

    return tasklists


def liststolist(lists):
    newlist = []
    for list in lists:
        for li in list:
            newlist.append(li)
    return newlist


# 替换字符串中内容
def arrangement(str, split, append):
    splits = str.split(split)
    ss = ''
    splen = len(splits)
    if splen > 0:
        for index, each in enumerate(splits):
            s = each.strip()
            if s == '':
                continue
            ss += s
            if index == (splen - 1):
                continue
            ss += append
    return ss


# 移除字符串最后一个字符
def removelastchar(str, char):
    index = str.find(char, len(str) - 1, len(str))
    if index > 0:
        return str[:index]
    return str


# 输出日志
def printlog(msg):
    if captureconfig.showlog:
        print(time_format_yyyymmddhhmmss2() + " " + str(msg))


# 去重(将list2中包含list1的内容去掉)
def removeduplicate(list1, list2):
    list1 = clean(list1)
    list2 = clean(list2)
    for list in list1:
        if list in list2:
            list2.remove(list)
    return list2


def clean(list):
    ls = []
    for l in list:
        ls.append(l.strip())
    return ls


def isfileexist(file):
    return os.path.exists(file)


def htmlformat(html):
    return BeautifulSoup(html, 'html.parser')


import json

if __name__ == '__main__':
    ss = '新闻资讯+阅读+资讯+新闻+男性+阅读教育+订阅+'
    # index = ss.find('+', len(ss) - 1, len(ss))
    # if index > 0:
    #     ss = ss[:index]
    #     print(ss)
    # ss = removelastchar(ss, '+')
    # print(ss)

    # li = [['lan', 'cong'], ['luo', 'heng']]
    # ls = liststolist(li)
    # for l in ls:
    #     printlog(l)

    content = openurl('http://p.3.cn/prices/mgets?skuIds=J_326154,J_&type=1')

    # js = json.loads(str(content))

    print(content)
    # printlog(content)

    import json

    pass
