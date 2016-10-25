# -*- coding: utf-8 -*-


from time import sleep

import captureutil


class JDBase(object):
    host = 'http://item.jd.hk/'
    suffix = '.html'

    # 设置cook
    def setcookie(self, cookie=None):
        self.cookie = cookie

    # 设置请求 user-agent
    def setua(self, useragent=None):
        self.useragent = useragent

    # 设置请求中的path
    def setrequestpath(self, requestpath):
        self.requestpath = str(requestpath).strip()
        path = self.requestpath
        self.url = self.host + self.requestpath + self.suffix
        url = self.url

    # 得到请求的path
    def getrequestpath(self):
        return self.requestpath

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
        captureutil.write(log.strip(), self.failedlog)

    # 保存成功日志
    def savesucceedlog(self, log):
        captureutil.write(log.strip(), self.succeedlog)

    # 保存结果
    def saveoutputlog(self, log):
        captureutil.write(log.strip(), self.outputlog)

    # 请求url
    def gethtml(self):

        url = self.url

        # print("request url: " + url)

        if self.cookie:
            return (captureutil.urlrequest(url, None, self.cookie, self.useragent), url)
        else:
            return (captureutil.urlrequest(url, None, None, self.useragent), url)

            # return captureutil.urlrequest(self.url, None)

    def sleep(self, start, end):
        sleep(captureutil.randnum(start, end))

    def setshowlog(self, showlog):
        self.showlog = showlog

    def getshowlog(self):
        return self.showlog

    def setresult(self, result):
        self.result = result

    def getresult(self):
        return self.result

    def setprice(self, price):
        self.price = price
        return self.price

    def getprice(self):
        return self.price
