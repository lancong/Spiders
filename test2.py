

import threading
import requests

import socket
import urllib.request


def openUrl(url):
    session = requests.session()
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    req = session.get(url, headers=headers)
    # req.encoding = "utf-8"
    # return BeautifulSoup(req.text, "html.parser")


class CheckProxyIP(object):
    url = 'http://zx.xvgs.pw/%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k.asp'

    def __init__(self, proxy_host, timeout=3, checkurl=url):
        self.host_temp = {"http": proxy_host}
        socket.setdefaulttimeout(3)
        self.checkremoteurl = checkurl
        pass

    def result(self):
        try:
            handler = urllib.request.ProxyHandler(self.host_temp)
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            opener = urllib.request.build_opener(handler, proxy_auth_handler)
            req = opener.open(self.checkremoteurl)
            # opener.open(self.checkremoteurl)
            print(req.code)
            # return 200 == req.code
        except:
            # return False
            pass

    pass


def request():
    url = 'http://zx.xvgs.pw/%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k%A1%EB31%20.%20f.%20%20%20s%20.%20.y.%20i%2C.l.%20%20x%20.%20%207%20%20%20.%20s%20o%20%20.%200%20.%204k.asp'

    while True:
        # captureutil.urlrequest(url)

        # openUrl(url)

        lines = open('proxyIps.txt')
        lines = lines.readlines()
        for line in lines:
            print("host: " + line)
            # break
            c = CheckProxyIP(line, 3, url)
            c.result()

    pass


if __name__ == '__main__':


    # request()

    threads = []
    for num in range(1, 300):
        th = threading.Thread(target=request)
        th.start()
        print("thread num: " + str(num))
        threads.append(th)

    for th in threads:
        th.join()

    pass
