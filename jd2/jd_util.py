# -*- coding: utf-8 -*-

import requests
import user_agent
import fetch_util

# 京东cookie字典
def jd_pc_cookie_dic(areaen):
    parameter_dic = {}
    if areaen == None:
        return parameter_dic
    if areaen.lower() == 'beijing':  # 北京朝阳区
        # 181809404.1907946185.1474426677.1474450676.1474463181.6
        parameter_dic["__jda"] = '181809404.1907946185.1474426677.1474450676.1474463181.6'
        # parameter_dic["__jdb"] = '181809404.2.1907946185|1.1474426677'
        parameter_dic["__jdc"] = '181809404'
        parameter_dic["__jdv"] = '181809404|direct|-|none|-'
        parameter_dic["areaId"] = '1'
        parameter_dic["ipLoc-djd"] = '1-72-4137-0'
        parameter_dic["ipLocation"] = '%u5317%u4EAC'
    elif areaen.lower() == 'guangzhou':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22gz%22%2C%22city%22%3A%22guangdong%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dgz%26city%3Dguangdong'
    elif areaen.lower() == 'shanghai':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22sh%22%2C%22city%22%3A%22shanghai%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dsh%26city%3Dshanghai'
    elif areaen.lower() == 'chengdu':
        parameter_dic["local_city"] = '%7B%20%22site%22%3A%22cd%22%2C%22city%22%3A%22sichuan%22%20%7D'
        parameter_dic["local_city_new"] = '%3Fsite%3Dcd%26city%3Dsichuan'
    return parameter_dic


# 取得地区cookies
def jd_pc_cookie(areaen):
    cookies = ''
    paramdic = jd_pc_cookie_dic(areaen)
    first = True
    for key in paramdic:
        if first:
            first = False
        else:
            cookies += ';'
        cookies += '{k}={v}'.format(k=key, v=paramdic[key])
    return cookies


# 为jd定制的网络请求(京东的请求中包含的信息比较多),请求失败会重试3次
def fetch(url, cookie=None, host=None, retry=0, timeout=8):
    headers = {
        'User-Agent': user_agent.pc(),
        'Host': host,
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        return session.get(url, timeout=timeout)
    except requests.RequestException:
        if retry < 3:
            fetch_util.print_log_debug("retry ... " + str(retry))
            return fetch(url, retry=retry + 1)
            # raise


# for jd price fetch
def fetch_for_price(url, request_item_url, timeout=8):
    headers = {
        "User-Agent": user_agent.pc(),
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Referer": request_item_url,
        "Host": 'p.3.cn',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        return session.get(url, timeout=timeout)
    except requests.RequestException:
        pass


if __name__ == '__main__':
    # ------------ 测试网络请求 ------------

    test_url = 'http://item.jd.hk/1000017.html'
    resp = fetch(test_url, jd_pc_cookie('beijing'), 'item.jd.hk')
    html = resp.text
    print(html)

    pass
