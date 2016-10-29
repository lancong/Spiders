# -*- coding: utf-8 -*-

import fetch_util

from jd import jdutil
from jd.jdbase import JDBase
from bs4 import BeautifulSoup

# 提取链接中的商品id,并返回价格
def get_price(url):
    return '\t>' + jdutil.jd_price(url)


class JDPage(JDBase):
    def __init__(self):
        JDBase.__init__(self)

    # 解析京东商品页面信息
    def parse_html_source(self):

        # 请求返回网页信息
        html_source = self.get_html_source()

        # 请求获取的html正文内容
        content = html_source[0]
        # 请求url
        request_url = html_source[1]

        # 将正文内容转换为一个BeautifulSoup对象
        html = BeautifulSoup(content, "html.parser")

        source = None
        type_match = 0

        while True:
            source = html.find("div", {'class': 'breadcrumb'})
            if source:
                type_match = 1
                # captureutil.printlog(request_url + " 匹配类型1")
                break
            source = html.find("div", {'id': 'itemInfo'})
            if source:
                type_match = 2
                # captureutil.printlog(request_url + " 匹配类型2")
                break
            source = html.find("div", {'class': 'crumb fl clearfix'})
            if source:
                type_match = 3
                # captureutil.printlog(request_url + " 匹配类型3")
                break

            type_match = 0
            break

        if type_match == 1:
            self.match_type1(html, request_url, source)
        elif type_match == 2:
            self.match_type2(request_url, source)
        elif type_match == 3:
            self.match_type3(html, request_url, source)
        else:
            self.match_failed(request_url)


    def match_failed(self, requesturl):
        self.set_print_log(requesturl + ' failed')
        self.set_result(False)

    def match_type3(self, html, requesturl, sources):
        divtext = sources.get_text()
        currentresult = requesturl + '\t' + fetch_util.replace_some_string(divtext, '\n', '')
        divitemname = html.find("div", {'class': 'sku-name'})
        if divitemname:
            itemname = divitemname.get_text()
            if itemname:
                currentresult += '>' + itemname

        price = get_price(requesturl)

        # 保存请求成功的path
        self.save_result(currentresult + price)
        self.set_print_log(requesturl + ' succeed')
        self.set_result(True)

    def match_type2(self, requesturl, sources):
        nametag = sources.find("div", {'id': 'name'})
        if nametag:
            h1itemname = nametag.find('h1')
            itemname = h1itemname.contents[0]
            if itemname:
                # 替换结果中的内容
                currentresult = fetch_util.replace_some_string(itemname, '>>', '>')

                price = get_price(requesturl)
                # 保存请求成功的path
                self.save_result(currentresult + price)
                self.set_print_log(requesturl + ' succeed')
                self.set_result(True)

    def match_type1(self, html, requesturl, sources):
        divtext = sources.get_text()
        currentresult = requesturl + '\t' + fetch_util.replace_some_string(divtext, '>', '>')
        itmenamehtml = html.find("div", {'id': 'name'})
        if itmenamehtml:
            h1itemname = itmenamehtml.find('h1')
            itemname = h1itemname.contents[0]
            if itemname:
                currentresult += '>' + itemname

        # 保存请求成功的path
        price = get_price(requesturl)
        self.save_result(currentresult + price)
        fetch_util.print_log(currentresult + price)
        self.set_print_log(requesturl + ' succeed')
        self.set_result(True)

    # 执行
    def execute(self):
        self.parse_html_source()


pass

if __name__ == '__main__':
    htmltext = fetch_util.urlrequest("http://p.3.cn/prices/mgets?skuIds=J_1000017,J_&type=1", None, None,
                                     fetch_util.get_pc_useragent(), None, None,
                                     10)
    print(htmltext)
    # html = BeautifulSoup(htmltext, "html.parser")
    # sources = html.find("div", {'class': 'crumb fl clearfix'})
    # print(sources)
    # divtext = sources.get_text()

    print(htmltext)
    # divtext = sources.get_text()
    # currentresult = captureutil.arrangement(divtext, '\n', '')
    #
    # print("1  " + divtext)
    # print("2  " + currentresult)

    # url = 'https://item.jd.com/3499302.html'
    #
    # indestart = url.rfind('/')
    # indexend = url.rfind('.')
    #
    # print(url[indestart + 1:indexend])
    #
    # print(indestart)
    # print(indexend)

    # flag = True
    # count = 0
    #
    # while flag:
    #     count += 1
    #
    #     if count == 2:
    #         flag = False
    #         break
    #
    #     print(str(count) + " test")
    #     pass

    pass
