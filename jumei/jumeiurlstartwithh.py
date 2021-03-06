# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jumei.jumeibase import JuMeiBase
import fetch_util


'''

处理类似如下的url

http://item.jumei.com/ht160807p2667554t2.html

不需要设置cookie

'''
class JumeiUrlStartWithH(JuMeiBase):
    def __init__(self):
        JuMeiBase.__init__(self)

    def findsource(self):

        contentall = self.gethtml()
        content = contentall[0]
        html = BeautifulSoup(content, "html.parser")
        sources = html.find("div", {'class': 'subpage_menu'})

        # 请求url
        requesturl = contentall[1]

        if sources:
            divtext = sources.get_text()
            currentresult = requesturl + '\t' + fetch_util.replace_some_string(divtext, '>', '>')

            # 保存请求成功的path
            self.saveoutputlog(currentresult)

            self.setshowlog(requesturl + ' succeed')
            self.setresult(True)

        else:
            sources = html.find("div", {'class': 'content_text'})

            if sources:
                tds = sources.findAll('td')
                title = ''
                if tds and len(tds) >= 1:
                    title = tds[0].get_text().strip() + tds[1].get_text().strip()
                else:
                    self.setshowlog(requesturl + ' failed')
                    self.setresult(False)
                    return
                if title:
                    currentresult = requesturl + '\t' + title
                else:
                    self.setshowlog(requesturl + ' failed')
                    self.setresult(False)
                    return

                # 保存请求成功的path
                self.saveoutputlog(currentresult)

                self.setshowlog(requesturl + ' succeed')
                self.setresult(True)

            else:

                self.setshowlog(requesturl + ' failed')
                self.setresult(False)
    # 执行
    def execute(self):

        self.findsource()