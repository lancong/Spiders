
# -*- coding: utf-8 -*-

import captureutil

from time import sleep

class JDBase(object):
    host = 'http://item.jd.hk/'
    suffix = '.html'

    # 设置cook
    def set_cookie(self, cookie=None):
        self.cookie = cookie

    # 设置请求 user-agent
    def set_useragent(self, useragent=None):
        self.useragent = useragent

    # 设置请求中的path
    def set_request_path(self, requestpath):
        self.requestpath = str(requestpath).strip()
        path = self.requestpath
        self.url = self.host + self.requestpath + self.suffix
        url = self.url

    # 得到请求的path
    def get_request_path(self):
        return self.requestpath

    # 设置请求url
    def set_request_url(self, url):
        self.url = url

    # 设置请求失败及错误的url,日志路径
    def set_failed_log_path(self, failedlog):
        self.failedlog = failedlog

    # 设置请求成功的url,日志路径
    def set_succeed_log_path(self, succeedlog):
        self.succeedlog = succeedlog

    # 结果输出位置
    def set_result_save_path(self, outputlog):
        self.outputlog = outputlog

    # 保存失败日志
    def save_failed_log(self, log):
        captureutil.write(log.strip(), self.failedlog)

    # 保存成功日志
    def save_succeed_log(self, log):
        captureutil.write(log.strip(), self.succeedlog)

    # 保存结果
    def save_result(self, log):
        captureutil.write(log.strip(), self.outputlog)

    # 请求url
    def get_html_source(self):

        url = self.url

        if self.cookie:
            return (captureutil.url_request_for_jd(url, None, self.cookie, self.useragent), url)
        else:
            return (captureutil.url_request_for_jd(url, None, None, self.useragent), url)

    def sleep(self, start, end):
        sleep(captureutil.randnum(start, end))

    def set_print_log(self, showlog):
        self.showlog = showlog

    def getshowlog(self):
        return self.showlog

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def set_price(self, price):
        self.price = price
        return self.price

    def get_price(self):
        return self.price
