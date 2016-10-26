# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from jd import jdutil
from jd.jdbase import JDBase

import captureutil


# 提取链接中的商品id,并返回价格
def getstoreprice(url):
    return '\t>' + jdutil.jd_price(url)


class JDPage(JDBase):
    def __init__(self):
        JDBase.__init__(self)

    def findsource(self):
        contentall = self.gethtml()

        # 请求获取的html正文内容
        content = contentall[0]
        # 请求url
        requesturl = contentall[1]

        # 将正文内容转换为一个BeautifulSoup对象
        html = BeautifulSoup(content, "html.parser")

        sources = None

        matchtype = 0

        while True:
            sources = html.find("div", {'class': 'breadcrumb'})
            if sources:
                matchtype = 1
                # captureutil.printlog(requesturl + " 匹配类型1")
                break
            sources = html.find("div", {'id': 'itemInfo'})
            if sources:
                matchtype = 2
                # captureutil.printlog(requesturl + " 匹配类型2")
                break
            sources = html.find("div", {'class': 'crumb fl clearfix'})
            if sources:
                matchtype = 3
                # captureutil.printlog(requesturl + " 匹配类型3")
                break

            matchtype = 0
            break

        if matchtype == 1:
            self.matchtag1(html, requesturl, sources)
        elif matchtype == 2:
            self.matchtag2(requesturl, sources)
        elif matchtype == 3:
            self.matchtag3(html, requesturl, sources)
        else:
            self.matchfailed(requesturl)

    def matchfailed(self, requesturl):
        self.setshowlog(requesturl + ' failed')
        self.setresult(False)

    def matchtag3(self, html, requesturl, sources):
        # divtext = sources.contents[0].strip()
        # if not divtext:
        divtext = sources.get_text()
        currentresult = requesturl + '\t' + captureutil.arrangement(divtext, '\n', '')
        divitemname = html.find("div", {'class': 'sku-name'})
        if divitemname:
            itemname = divitemname.get_text()
            if itemname:
                currentresult += '>' + itemname

        price = getstoreprice(requesturl)

        # 保存请求成功的path
        self.saveoutputlog(currentresult + price)
        self.setshowlog(requesturl + ' succeed')
        self.setresult(True)

    def matchtag2(self, requesturl, sources):
        nametag = sources.find("div", {'id': 'name'})
        if nametag:
            h1itemname = nametag.find('h1')
            itemname = h1itemname.contents[0]
            if itemname:
                # 替换结果中的内容
                currentresult = captureutil.arrangement(itemname, '>>', '>')

                price = getstoreprice(requesturl)
                # 保存请求成功的path
                self.saveoutputlog(currentresult + price)
                self.setshowlog(requesturl + ' succeed')
                self.setresult(True)

                # divtext = sources.get_text()
                # currentresult = requesturl + '\t' + captureutil.arrangement(divtext, '>', '>')

                # 保存请求成功的path
                # self.saveoutputlog(currentresult)

    def matchtag1(self, html, requesturl, sources):
        divtext = sources.get_text()
        currentresult = requesturl + '\t' + captureutil.arrangement(divtext, '>', '>')
        itmenamehtml = html.find("div", {'id': 'name'})
        if itmenamehtml:
            h1itemname = itmenamehtml.find('h1')
            itemname = h1itemname.contents[0]
            if itemname:
                currentresult += '>' + itemname

        # print('current info: ' + currentresult)
        # 保存请求成功的path
        price = getstoreprice(requesturl)
        self.saveoutputlog(currentresult + price)
        captureutil.printlog(currentresult + price)
        self.setshowlog(requesturl + ' succeed')
        self.setresult(True)

    # 执行
    def execute(self):
        self.findsource()


pass

if __name__ == '__main__':
    htmltext = captureutil.urlrequest("http://p.3.cn/prices/mgets?skuIds=J_1000017,J_&type=1", None, None,
                                      captureutil.getpcua(), None, None,
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
