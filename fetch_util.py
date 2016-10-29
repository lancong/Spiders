# -*- coding: utf-8 -*-

import os
import gzip
import time
import random
import urllib
import codecs
import requests
import fetch_config
import urllib.request
import user_agent

from io import StringIO
from http import cookiejar
from bs4 import BeautifulSoup
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


# 网络请求,并返回页面
def url_request_for_jd(url, referurl=None, cookie=None, useragent=None, postdata=None, ip=None, timeout=60):
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
    req.add_header('Host', 'item.jd.hk')
    req.add_header('Upgrade-Insecure-Requests', '1')

    # Host:item.jd.hk
    # Upgrade-Insecure-Requests:1

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


def open_url(url):
    session = requests.session()
    headers = {
        "User-Agent": get_pc_useragent(),
        "Accept": "text/html,application/xhtml+xml,application/xml"}
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    req = session.get(url, headers=headers)
    req.encoding = "utf-8"
    # return BeautifulSoup(req.text, "html.parser")
    return req.text


def openurl2(url, refererurl, host='p.3.cn'):
    session = requests.session()
    headers = {
        "User-Agent": get_pc_useragent(),
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Referer": refererurl,
        "Host": host,
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    req = session.get(url, headers=headers)
    req.encoding = "utf-8"
    # return BeautifulSoup(req.text, "html.parser")
    return req.text


# pc user-agent
def get_pc_useragent():
    ua = user_agent.for_pc
    index = randnum(0, len(ua) - 1)
    return ua[index]


# mobile user-agent
def get_mobile_useragent():
    ua = user_agent.for_mobile
    index = randnum(0, len(ua) - 1)
    return ua[index]


# 时间格式 20160202
def get_time_yyyymmdd():
    return time.strftime("%Y%m%d", time.localtime(time.time()))


# 时间格式 2016-02-02
def get_time_yyyymmdd2():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


# 时间格式 19:24:25
def get_time_hhmmss():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


# 时间格式 20160202112222
def get_time_yyyymmddhhmmss():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


# 时间格式 2016-02-02 11:22:22
def time_format_yyyymmddhhmmss2():
    return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))


def mkdirs(path):
    path = path.strip()
    path = path.rstrip("/")
    if not os.path.exists(path):
        os.makedirs(path)


# 读取内容并非全部加载入内存
def read(fpath):
    BLOCK_SIZE = 4086
    with open(fpath, 'r') as f:
        while True:
            block = f.readlines(BLOCK_SIZE)
            if block:
                yield block
            else:
                return


def write(data, path, mode="a", charset='utf-8', newline=True):
    with codecs.open(path, mode, charset) as writer:
        writer.write(data)
        if newline:
            writer.write("\r\n")
        writer.flush()


# 生成随机整形数字
def randnum(minnum, maxnum):
    return random.randint(minnum, maxnum)


# 编码URL中字符
def urlencode(text):
    return quote(str(text))


# 删除文件
def file_delete(file):
    if os.path.exists(file):
        os.remove(file)


# 分发任务
def task_dispatch(lists, threadnum):
    # 任务总列表
    tasklists = []

    # 单线程不拆分任务
    if threadnum < 1:
        tasklists.append(lists)
        return tasklists

    # list size
    listsize = len(lists)

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

    print_log("thread queue: " + str(len(tasklists)) + '\t\n')

    return tasklists


def liststolist(lists):
    newlist = []
    for list in lists:
        for li in list:
            newlist.append(li)
    return newlist


# 替换字符串中内容
def replace_some_string(str, split, append):
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
def remove_last_char(str, char):
    index = str.find(char, len(str) - 1, len(str))
    if index > 0:
        return str[:index]
    return str


# 输出日志
def print_log(msg):
    if fetch_config.print_log:
        print(time_format_yyyymmddhhmmss2() + " " + str(msg))


# 调度日志
def print_log_debug(msg):
    if fetch_config.print_debug_log:
        print(time_format_yyyymmddhhmmss2() + " " + str(msg))


# 去重(将list2中包含list1的内容去掉)
def remove_duplicate(list1, list2):
    for list in list1:
        list = list.strip()
        if list in list2:
            list2.remove(list)
    return list2


def clean(list):
    ls = []
    for l in list:
        ls.append(l.strip())
    return ls


# byte to str
def byte_to_str(byte):
    result = ''
    try:
        result = byte.decode()
    except:
        return result
    return result


def file_exist(file):
    return os.path.exists(file)


def to_bs_object(html):
    return BeautifulSoup(html, 'html.parser')


import json

if __name__ == '__main__':
    #
    # num = 0
    # while True:
    #     num += 1
    #     print(get_pc_useragent())
    #     if num == 20:
    #         break

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

    # Referer:https://item.jd.com/10478786444.html
    # content = openurl('http://p.3.cn/prices/mgets?skuIds=J_326154,J_&type=1')

    # js = json.loads(str(content))

    # print(content)
    # printlog(content)

    import json

    # https://p.3.cn/prices/mgets?callback=jQuery7955799&type=1&area=1_72_4137_0&pdtk=&pduid=531394193&pdpin=&pdbp=0&skuIds=J_10478786444
    # while True:
    #     ss = randnum(1000000, 8888888)
    #     print(ss)

    # def read(fpath):
    #     BLOCK_SIZE = 4086
    #     with codecs.open(fpath, 'r') as f:
    #         while True:
    #             block = f.readlines(BLOCK_SIZE)
    #             if block:
    #                 yield block
    #             else:
    #                 return
    #
    #
    # file = read('jdurlall.txt')
    #
    # # print(type(file.__next__()))
    #
    # lss = file.__next__()
    #
    # print(type(lss))
    # print(file.__next__())
    # print(file.__next__())
    # print(file.__next__())
    # print(file.__next__())
    # for l in lss:
    #     print(l.strip() == '3301200')
    #     print(type(l))

    # print("haha",str(file.__next__()))
    # print("haha2",str(file.__next__()))
    # # print("haha3",str(file.__next__()))


    pass
