# -*- coding: utf-8 -*-

from jumei.jumeiurlstartwithnum import JumeiUrlStartWithNum
import captureutil
from bs4 import BeautifulSoup

if __name__ == '__main__':

    dirpath = '/Users/Lan/TestDir/output/'
    succeed = dirpath + 'sc.log'
    failed = dirpath + 'fl.log'
    out = dirpath + 'rs.log'

    jumei = JumeiUrlStartWithNum()

    jumei.setsucceedlog(succeed)
    jumei.setfailedlog(failed)
    jumei.setshowlog(out)

    jumei.setcookie(None)
    jumei.setua(captureutil.get_pc_useragent())
    jumei.setrequestpath("847191")

    jumei.findsource()

    pass
