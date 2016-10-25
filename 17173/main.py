# -*- coding: utf-8 -*-

import codecs
import gzip
import os
import threading
from http import cookiejar
from io import StringIO
import random
import time
import urllib
import urllib.request
from bs4 import BeautifulSoup

import captureconfig

outfile = '/Users/Lan/TestDir/output/17173_yeyou.txt'
outfilebak = '/Users/Lan/TestDir/output/17173_yeyou_url_bak.txt'


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


# 时间格式 2016-02-02 11:22:22
def time_format_yyyymmddhhmmss2():
    return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))


# 输出日志
def printlog(msg):
    print(time_format_yyyymmddhhmmss2() + " " + msg)


# 整理文字
def arrangement(str, split, append):
    splits = str.split(split)
    ss = ''
    splen = len(splits)
    if splen > 0:
        for index, each in enumerate(splits):
            ss += each.strip()
            if index == (splen - 1):
                continue
            ss += append
    return ss


# 生成随机整形数字
def randnum(minnum, maxnum):
    return random.randint(minnum, maxnum)


# pc user-agent
def getpcua():
    ua = captureconfig.user_agent_pc
    index = randnum(0, len(ua) - 1)
    return ua[index]
    pass


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


# 去重(将list2中包含list1的内容去掉)
def removeduplicate(list1, list2):
    for list in list1:
        if list in list2:
            list2.remove(list)
    return list2


# 分发任务
def dispatchtask(lists, threadnum):
    # 单线程不拆分任务
    if threadnum < 1:
        return lists

    # list size
    listsize = len(lists)

    if threadnum > listsize:
        return lists

    single_task_num = int(listsize / threadnum)

    # 任务总列表
    tasklists = []
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


def gamelist(url):
    source = urlrequest(url, None, None, getpcua())
    html = BeautifulSoup(source, 'html.parser')
    gameinfos = html.findAll('li', {'class': 'list-item'})

    host = 'http://game.yeyou.com'

    for index in range(len(gameinfos)):
        singlehtml = gameinfos[index]

        url = singlehtml.find('a')['href']

        info = singlehtml.find('span', {'class': 'txt'})
        text = info.get_text()
        text = arrangement(text, '\n', ' ')

        out = host + url + '\t' + text

        # printlog(host + url)

        write(out, outfile)

def singletask(tasks):
    taskslen = len(tasks)
    count = 0
    for task in tasks:
        count += 1
        gamelist(task)
        printlog('[' + str(count) + '/' + str(taskslen) + ']' + ' ' + task)
        write(task, outfilebak)
        time.sleep(randnum(10, 40))


if __name__ == '__main__':

    threadnum = 15

    urlformat = 'http://game.yeyou.com/list-0-0-0-0-0-0-0-0-0-0-3-0-1.html?page='

    urls = []

    for index in range(1, 138):
        urls.append(urlformat + str(index))

    fetchedurls = []

    if os.path.exists(outfilebak):
        hasfetch = open(outfilebak, 'r')
        fetchedurls = hasfetch.readlines()

    urls = removeduplicate(fetchedurls, urls)

    tasks = dispatchtask(urls, threadnum)

    threads = []

    for task in tasks:
        th = threading.Thread(target=singletask, args=(task,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    pass
