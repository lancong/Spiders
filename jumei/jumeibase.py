# -*- coding: utf-8 -*-
from time import sleep

import fetch_util

'''

聚美超类

'''


class JuMeiBase(object):
    host = 'http://item.jumei.com/'
    suffix = '.html'

    # 设置cook
    def setcookie(self, cookie=None):
        self.cookie = cookie

    # 设置请求 user-agent
    def setua(self, useragent=None):
        self.useragent = useragent

    # 设置请求中的path
    def setrequestpath(self, requestpath):
        self.requestpath = requestpath
        self.url = self.host + self.requestpath.strip() + self.suffix

    # 设置请求url
    def setrequesturl(self, url):
        self.url = url

    # 设置请求失败及错误的url,日志路径
    def setfailedlog(self, failedlog):
        self.failedlog = failedlog

    # 设置请求成功的url,日志路径
    def setsucceedlog(self, succeedlog):
        self.succeedlog = succeedlog

    # 结果输出位置
    def setoutputlog(self, outputlog):
        self.outputlog = outputlog

    # 保存失败日志
    def savefailedlog(self, log):
        fetch_util.write(log.strip(), self.failedlog)

    # 保存成功日志
    def savesucceedlog(self, log):
        fetch_util.write(log.strip(), self.succeedlog)

    # 保存结果
    def saveoutputlog(self, log):
        fetch_util.write(log.strip(), self.outputlog)

    # 请求url
    def gethtml(self):
        url = self.url

        if self.cookie:
            return fetch_util.urlrequest(url, None, self.cookie, self.useragent), url
        else:
            return fetch_util.urlrequest(url, None, None, self.useragent), url

        # return captureutil.urlrequest(self.url, None)

    def sleep(self, start, end):
        sleep(fetch_util.randnum(start, end))

    def setshowlog(self, showlog):
        self.showlog = showlog

    def getshowlog(self):
        return self.showlog

    def setresult(self, result):
        self.result = result

    def getresult(self):
        return self.result
