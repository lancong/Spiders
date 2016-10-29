# -*- coding: utf-8 -*-

import threading
from time import sleep

import fetch_util
from bs4 import BeautifulSoup


# 得到大分类下的url
class MainCategoryUrls():
    def __init__(self, url):
        self.url = url
        self.html = None
        self.gethtml()

    def gethtml(self):
        content = fetch_util.urlrequest(self.url, None, None, useragent=fetch_util.get_pc_useragent())
        self.html = BeautifulSoup(content, 'html.parser')

    def geturls(self):
        ul = self.html.find('ul', {'class': 'switch-tab cate-tab'})
        lis = ul.findAll('li')
        urls = []
        for li in lis:
            if 'class' in li.attrs:
                continue
            a = li.find('a')
            if 'href' in a.attrs:
                urls.append(a['href'])
        return urls


# 父类页面(包含很多app)
class ParentPage():
    def __init__(self, url):
        self.url = url
        self.pagenum = 1
        self.html = None
        # 初始化页面内容
        self.gethtml()

    # 得到页面内容
    def gethtml(self):
        content = fetch_util.urlrequest(self.url, None, None, useragent=fetch_util.get_pc_useragent())
        self.html = BeautifulSoup(content, 'html.parser')

    # 返回基准url和页面最大数
    def getpageinfo(self):
        pagenuminfo = self.html.find('div', {'class': 'page-wp roboto'})
        if pagenuminfo:
            atags = pagenuminfo.findAll('a')
            if atags:
                baseurl = None
                pagenummax = 0
                isfind = False
                for tag in atags:
                    tagattrs = tag.attrs

                    if 'href' in tagattrs:
                        # print(tag['href'])
                        # print(tag.get_text() + '\t\n')

                        # remoteurl = tag['href']

                        # 页面数
                        pageindex = tag.get_text()

                        if pageindex.isdigit():
                            num = int(pageindex)

                            if not isfind and not 'page-item' in tagattrs:
                                isfind = True
                                baseurl = tag['href']

                            # if not isfind and num == 1:
                            #     baseurl = tag['href']
                            #     isfind = True

                            if num > pagenummax:
                                pagenummax = num

                if baseurl:
                    return baseurl, pagenummax
        else:
            return None

    # 得到当前分类下所有需要请求的urls
    def getpageurls(self):
        paginfo = self.getpageinfo()

        urls = []

        if paginfo:
            baseurl = paginfo[0]
            maxnum = paginfo[1]

            for index in range(1, maxnum + 1):
                urls.append(baseurl + '_' + str(index))

        return urls


class ParentPageUrl():
    def __init__(self, url):
        self.url = url
        self.html = None
        # 初始化页面内容
        self.gethtml()

    def gethtml(self):
        content = fetch_util.urlrequest(self.url, None, None, useragent=fetch_util.get_pc_useragent())
        self.html = BeautifulSoup(content, 'html.parser')

    # 得到当前类别
    def getcategory(self):
        category = self.html.find('div', {'class': 'crumb'})
        # if 'get_text' in category.attrs:
        try:
            category = category.get_text()
        # else:
        except:
            category = ''
        return fetch_util.replace_some_string(category, '\n', '')

    # 得到当前页面的需要请求的urls
    def getcurpageurls(self):
        ul = self.html.find('ul', {'id': 'j-tag-list'})
        urls = []
        if ul:
            lis = ul.findAll('li', {'class': 'card'})
            for li in lis:
                atag = li.find('a')
                if 'href' in atag.attrs:
                    urls.append(atag['href'])
        return urls


class PageInfo():
    def __init__(self, url):
        self.url = url
        self.html = None
        self.info = None
        self.init()

    def gethtml(self):
        content = fetch_util.urlrequest(self.url, None, None, useragent=fetch_util.get_pc_useragent())
        self.html = BeautifulSoup(content, 'html.parser')
        pass

    def init(self):
        # 初始化页面内容
        self.gethtml()
        # 得到应用详细信息
        self.getappinfo()

    # 得到应用详细信息
    def getappinfo(self):
        self.info = self.html.find('dl', {'class': 'infos-list'})
        # print(self.info)

    # 得到分类
    def getcategory(self):
        if self.info:
            category = self.info.find('dd', {'class': 'tag-box'})
            if category:
                s = category.get_text()
                s = fetch_util.replace_some_string(s, "\n", '+')
                return fetch_util.remove_last_char(s, '+')

    # 得到标签
    def gettag(self):
        if self.info:
            tag = self.info.find('div', {'class': 'side-tags clearfix'})
            if tag:
                s = tag.get_text()
                s = fetch_util.replace_some_string(s, "\n", '+')
                return fetch_util.remove_last_char(s, '+')

    # 得到应用名称
    def getappname(self):
        appinfo = self.html.find('div', {'class': 'app-info'})
        if appinfo:
            appanme = appinfo.find('span', {'class': 'title'})
            if appanme:
                return appanme.get_text().strip()
        return 'unknow'


def func(lists, maincategory, outfile):
    if lists and len(lists) > 0:

        alllen = len(lists)
        count = 0

        for currenturl in lists:

            count += 1

            pageinfo = PageInfo(currenturl)
            appname = pageinfo.getappname()
            category = pageinfo.getcategory()
            if not category:
                category = 'unknow'
            tag = pageinfo.gettag()
            if not tag:
                tag = 'unknow'

            # 打印日志
            # captureutil.printlog(currenturl + '\t' + appname)
            fetch_util.print_log('[' + str(count) + '/' + str(alllen) + '] ' + currenturl)

            outinfo = currenturl + '\t' + maincategory + '>' + appname + '\tc:' + category + '\tt:' + tag

            # 写入结果
            fetch_util.write(outinfo, outfile)

            # 随机休眠几秒
            sleep(fetch_util.randnum(10, 40))


def main():

    # 指定大类别url
    outfile = '/Users/Lan/TestDir/out/wandoujia.txt'
    # 文件输出位置
    specurls = ['http://www.wandoujia.com/category/396']


    # outfile = wandoujiaconfig.outfile

    # specurls = wandoujiaconfig.specurls

    # specurls = ['http://www.wandoujia.com/category/382', 'http://www.wandoujia.com/category/388',
    #             'http://www.wandoujia.com/category/402', 'http://www.wandoujia.com/category/392']

    allurls = []

    fetch_util.print_log('update request urls ...')

    for specurl in specurls:
        maincategoryurls = MainCategoryUrls(specurl)
        url = maincategoryurls.geturls()
        allurls.append(url)

    urls = fetch_util.liststolist(allurls)

    fetch_util.print_log('update request urls finished, len: ' + str(len(urls)))

    for url in urls:

        parentpage = ParentPage(url=url)
        requesturls = parentpage.getpageurls()
        if requesturls and len(requesturls) > 0:
            for requesturl in requesturls:
                parentpageurl = ParentPageUrl(requesturl)
                # 当前主大类别
                maincategory = parentpageurl.getcategory()
                if not maincategory:
                    maincategory = 'unknow'
                # 当前页面可请求urls
                currenturls = parentpageurl.getcurpageurls()

                if currenturls and len(currenturls) > 0:

                    tasks = fetch_util.task_dispatch(currenturls, 10)

                    threads = []

                    for task in tasks:
                        th = threading.Thread(target=func, args=(task, maincategory, outfile))
                        th.start()
                        threads.append(th)
                        pass

                    for th in threads:
                        th.join()

        # 写入结果
        fetch_util.write('\r\n------ i am line -----\r\n', outfile)
        fetch_util.print_log("has finish: " + url)

        sleep(fetch_util.randnum(10, 30))


# def main():
#     parentpage = ParentPage('http://www.wandoujia.com/category/388')
#     parentpage.gethtml()
#     # res = prentPage.getpageinfo()
#     # print(res)
#     urls = parentpage.getpageurls()
#
#     for url in urls:
#         print(url)

# def main2():
#     child = FixChildUrl('http://www.wandoujia.com/category/388')
#     # child.gethtml()
#     # ss = child.getcategory()
#     # ss = captureutil.arrangement(ss, '\n', '')
#     # print(ss)
#     urls = child.getcurpageurls()
#     for url in urls:
#         print(url)
#     pass


# def main3():
#     page = PageInfo('http://www.wandoujia.com/apps/com.ss.android.article.news')
#     appname = page.getappname()
#     category = page.getcategory()
#     # category = captureutil.arrangement(category, "\n", '+')
#     tag = page.gettag()
#     # tag = captureutil.arrangement(tag, "\n", '+')
#
#     print(appname + "\t\n *******")
#     print(category + "\t\n *******")
#     print(tag + "\t\n *******")
#     pass



if __name__ == '__main__':


    # specurls = ['http://www.wandoujia.com/category/382', 'http://www.wandoujia.com/category/388',
    #             'http://www.wandoujia.com/category/402', 'http://www.wandoujia.com/category/392']
    #
    # allurls = []
    #
    # captureutil.printlog('update request urls ...')
    #
    # for specurl in specurls:
    #     maincategoryurls = MainCategoryUrls(specurl)
    #     url = maincategoryurls.geturls()
    #     allurls.append(url)
    #
    # urls = captureutil.liststolist(allurls)
    #
    # captureutil.printlog('update request urls finished, len: ' + str(len(urls)))



    main()


    # main2()
    # main3()
    # print('1'.isdigit())

    # maincategoryurls = MainCategoryUrls('http://www.wandoujia.com/category/388')
    # urls = maincategoryurls.geturls()
    # for url in urls:
    #     print(url)

    # specurl = ['http://www.wandoujia.com/category/382', 'http://www.wandoujia.com/category/388',
    #            'http://www.wandoujia.com/category/402', 'http://www.wandoujia.com/category/392']
    #
    # for url in specurl:
    #     print(url)

    # specurls = ['http://www.wandoujia.com/category/382', 'http://www.wandoujia.com/category/388',
    #             'http://www.wandoujia.com/category/402', 'http://www.wandoujia.com/category/392']
    #
    # allurls = []
    #
    # captureutil.printlog('fetch request urls ...')

    # maincategoryurls = MainCategoryUrls(specurls[2])
    # url = maincategoryurls.geturls()
    # allurls.append(url)

    # for specurl in specurls:
    #     maincategoryurls = MainCategoryUrls(specurl)
    #     url = maincategoryurls.geturls()
    #     allurls.append(url)
    #
    # captureutil.printlog('fetch request urls finished, len:' + str(len(allurls)))
    #
    # for url in allurls:
    #     print(url)


    # page = ParentPage('http://www.wandoujia.com/category/392')
    # urls = page.getpageurls()
    #
    # for url in urls:
    #     print(url)


    # <a class="page-item current" href="http://www.wandoujia.com/category/392">1</a>
    #
    # a = '<a class="page-item current" href="http://www.wandoujia.com/category/392">1</a>'
    #
    # html = captureutil.htmlformat(a)
    #
    # html = html.find('a')
    #
    #
    # ss = html['class']



    # print(html)

    # print(html['href'])

    # print(html['class'])

    # for attr in html.attrs:



        # print(html[attr])
        # print(attr)
        # print(html[attr])
        # print(html.attrs[attr])
    # print('finish')
    pass
