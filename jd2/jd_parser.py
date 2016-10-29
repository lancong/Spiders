# -*- coding: utf-8 -*-

import json
import random
from time import sleep

import fetch_util
import task_dispatch

from jd2 import jd_util

'''

这些方法是解析页面信息,获取面包屑的标题信息

每次如果要爬取新内容,记得更新cookie的信息,及商品请求的url

'''

host = 'http://item.jd.hk/'
suffix = '.html'

# redis任务表
redis_task_key = 'jd_20161024'
# redis成功与失败记录表
redis_succeed_count_key = 'jd_20161024_succeed'
redis_failed_count_key = 'jd_20161024_failed'


# 拼接请求url
def make_request_url(queue, redis_client):
    try:
        queun_info = queue.get(block=False, timeout=10)
    except:
        raise

    url_path = fetch_util.byte_to_str(queun_info[0])
    # task_dispatch.sign_task(redis_client, redis_task_key, url_path, 1)
    return host + url_path + suffix, url_path


# 请求页面
def get_html(url, cookie=None, host=None):
    resp = jd_util.fetch(url, cookie, host)
    if 200 == resp.status_code:
        return resp.text
    else:
        return ''


# 解析页面
def parse_html(html):
    if not html:
        return ''

    # 将正文内容转换为一个BeautifulSoup对象
    html = fetch_util.to_bs_object(html)
    # 得到合适的页面解析类型
    parser_type_source = get_parser_type_and_source(html)
    # 得到页面解析结果
    return get_parser_result(html, parser_type_source)


# 得到商品价格
def get_item_price(request_item_url, item_id):
    rand_num = str(random.randint(1000000, 8888888))
    request_price_url = 'http://p.3.cn/prices/mgets?callback=jQuery' + rand_num + '&type=1&area=1_72_4137_0&pdtk=&pduid=531394193&pdpin=&pdbp=0&skuIds=J_' + item_id
    resp = jd_util.fetch_for_price(request_price_url, request_item_url)
    # jQuery3493581([{"id":"J_10550439205","p":"79.00","m":"199.00","op":"106.00"}]);
    price_json_str = resp.text

    start = price_json_str.find('{')
    end = price_json_str.find('}')
    price_json = price_json_str[start:end + 1]

    try:
        js = json.loads(price_json)
        if 'p' in js:
            return js['p']
    except:
        return '-1.00'


# 保存结果
def save_result(path, request_url, bread_tag_name, price):
    if bread_tag_name:
        save_info = request_url + '\t' + bread_tag_name + '\t' + price
        fetch_util.print_log(request_url + ' succeed')
        fetch_util.print_log_debug(save_info)

        fetch_util.print_log_debug("path: " + path)

        if path:
            fetch_util.write(save_info, path)
        else:
            fetch_util.print_log('****** 未设置结果存储路径!!! ******')
    else:
        fetch_util.print_log(request_url + ' failed')


# 保存执行结果到redis
def update_redis(redis_client, result, item_id):
    if result:
        # 更新redis执行结果状态
        task_dispatch.sign_task(redis_client, redis_task_key, item_id, 2)
        # 成功计数加1
        task_dispatch.count_result(redis_client, redis_succeed_count_key)
    else:
        # 更新redis执行结果状态
        task_dispatch.sign_task(redis_client, redis_task_key, item_id, 3)
        # 失败计数加1
        task_dispatch.count_result(redis_client, redis_failed_count_key)


# --------------------- 页面解析方法 ---------------------

# 判断合适的页面解析者
def get_parser_type_and_source(html):
    source = html.find("div", {'class': 'breadcrumb'})
    if source:
        fetch_util.print_log_debug("匹配类型1")
        return 1, source
    source = html.find("div", {'id': 'itemInfo'})
    if source:
        fetch_util.print_log_debug("匹配类型2")
        return 2, source
    source = html.find("div", {'class': 'crumb fl clearfix'})
    if source:
        fetch_util.print_log_debug("匹配类型3")
        return 3, source
    # 未匹配类型
    return 0, None


# 得到页面解析者返回的结果
def get_parser_result(html, type_and_source):
    parser_type = type_and_source[0]
    source = type_and_source[1]

    bread_tag_name = ''

    if 1 == parser_type:
        bread_tag_name = parser_type_1(html, source)
    elif 2 == parser_type:
        bread_tag_name = parser_type_2(html, source)
    elif 3 == parser_type:
        bread_tag_name = parser_type_3(html, source)
    else:
        # 失败的类型(此商品id不存在,跳转到主页)
        pass

    return bread_tag_name


# 解析类型1
def parser_type_1(html, source):
    div_text = source.get_text()
    result = fetch_util.replace_some_string(div_text, '>', '>')
    item_name_tag = html.find("div", {'id': 'name'})
    if item_name_tag:
        h1_item_name = item_name_tag.find('h1')
        item_name = h1_item_name.contents[0]
        if item_name:
            result += '>' + item_name
    return result


# 解析类型2
def parser_type_2(html, source):
    bread_tag = source.find("div", {'id': 'name'})
    if bread_tag:
        h1_item_name = bread_tag.find('h1')
        item_name = h1_item_name.contents[0]
        if item_name:
            # 替换结果中的内容
            result = fetch_util.replace_some_string(item_name, '>>', '>')
            return result
    return ''


# 解析类型3
def parser_type_3(html, source):
    div_text = source.get_text()
    result = fetch_util.replace_some_string(div_text, '\n', '')
    item_name_tag = html.find("div", {'class': 'sku-name'})
    if item_name_tag:
        item_name = item_name_tag.get_text()
        if item_name:
            result += '>' + item_name
    return result


# --------------------- 任务从spider开始 ---------------------


# jd爬虫任务
def jd_spider_task(queue, redis_client, cookie=None, host=None, path=None):
    # 拼接url
    request_url_info = make_request_url(queue, redis_client)
    # 商品请求url
    request_url = request_url_info[0]
    # 商品id
    item_id = request_url_info[1]
    # 请求页面
    html = get_html(request_url, cookie, host)
    # 得到页面解析结果
    parse_result = parse_html(html)

    # 得到商品价格
    item_price = get_item_price(request_url, item_id)
    # 保存信息
    save_result(path, request_url, parse_result, item_price)

    # 更新redis信息
    update_redis(redis_client, parse_result, item_id)

    # 休眠
    sleep(5)


def task(queue, redis_client, cookie, host, result_save_path):
    while True:
        jd_spider_task(queue, redis_client, cookie, host, result_save_path)


# 测试指定页面
def parse_specail_url(url):
    html = get_html(url)
    return parse_html(html)


if __name__ == '__main__':

    # 测试指定页面,数据是否能够提取
    url = 'http://item.jd.hk/1000017.html'
    print(parse_specail_url(url))


    pass
