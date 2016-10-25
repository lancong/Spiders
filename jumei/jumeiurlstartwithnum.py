# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jumei.jumeibase import JuMeiBase
import captureutil

'''

处理类似如下的url

http://item.jumei.com/2787031.html

需要设置cookie

'''


class JumeiUrlStartWithNum(JuMeiBase):
    def __init__(self):
        JuMeiBase.__init__(self)

    def findsource(self):

        contentall = self.gethtml()
        content = contentall[0]
        html = BeautifulSoup(content, "html.parser")
        sources = html.find("div", {'id': 'mall_detail_sub'})

        # 请求url
        requesturl = contentall[1]

        if sources:
            divtext = sources.get_text()
            currentresult = requesturl + '\t' + captureutil.arrangement(divtext, '>', '>')

            # 保存请求成功的path
            self.saveoutputlog(currentresult)

            self.setshowlog(requesturl + ' succeed')
            self.setresult(True)

        else:
            sources = html.find("div", {'class': 'breadcrumbs'})
            if sources:
                divtext = sources.get_text()
                currentresult = requesturl + '\t' + captureutil.arrangement(divtext, '>', '>')

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
