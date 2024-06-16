# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : get_proxy.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/27 9:58
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/27 9:58 
@Version            : 1.0
@Description        : get free proxies from kuaidaili, no https, only http
"""
import json
import re

import requests
from lxml import etree
import time

proxy_urls = [
    f"https://www.kuaidaili.com/free/inha/{page}/"
    for page in range(1, 1 + 1)
]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Referer': 'https://www.kuaidaili.com/free/inha/1',
    'Sec-Ch-Ua': 'Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "macOS",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}

# 定义1个字典表示单个 proxy、1个列表存储全部 proxy
proxy = {}
proxy_list = []


# 23年的方案。当时 requests 能拿到渲染好后的页面，结合 xpath 提取内容
def get_proxy_requests_xpath():
    for url in proxy_urls:
        print(url)
        response = requests.get(url, headers=headers)
        html = response.text

        # selector 的类型是 <class 'lxml.etree._Element'>
        selector = etree.HTML(html)

        # xpath 路径会随着网页改版而变化，请以最新页面路径为准
        # trs 的类型是 <class 'list'>
        trs = selector.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')

        for tr in trs:
            # tr 的类型还是 <class 'lxml.etree._Element'>
            # print(type(tr))
            ip = tr.xpath("./td[1]/text()")[0]
            port = tr.xpath("./td[2]/text()")[0]
            position = tr.xpath("./td[5]/text()")[0]
            res_speed = tr.xpath("./td[6]/text()")[0]
            last_verify = tr.xpath("./td[7]/text()")[0]

            proxy["http"] = f"http://{ip}:{port}/"
            proxy["https"] = f"http://{ip}:{port}/"
            proxy["position"] = position
            proxy["res_speed"] = res_speed
            proxy["last_verify"] = last_verify
            print(proxy)
            proxy_list.append(proxy)
        time.sleep(2)

    return proxy_list


# 24年的方案，网页不再直接返回渲染后的页面，而是数据+JavaScript
# 还用 xpath 提取信息，但是把 requests 换成了 requests_html
# 通过 使用 session 机制，调用 r.html.render() 得到通过 JavaScript 后的数据
def get_proxy_requests_html_xpath():
    from requests_html import AsyncHTMLSession, HTMLSession
    asession = AsyncHTMLSession()
    session = HTMLSession()

    async def process():
        r = await asession.get('https://www.kuaidaili.com/free/inha/1/', headers=headers)
        await r.html.arender()
        return r

    # 因为页面渲染需要时间，所以要么无脑等待，要么用异步函数
    # resp = asession.run(process)[0]

    resp = session.get('https://www.kuaidaili.com/free/inha/1/', headers=headers)

    # 可以把渲染前后的页面文本抓下来，做个对比
    # with open('before.html', 'w', encoding='utf-8') as f:
    #     f.write(resp.html.html)

    resp.html.render()

    # with open('after.html', 'w', encoding='utf-8') as f:
    #     f.write(resp.html.html)

    # resp.html.html 类型是 <class 'str'>
    # resp.html 类型是 <class 'requests_html.HTML'>
    print(type(resp.html))

    # trs 得到的是 list 类型
    trs = resp.html.xpath('//*[@id="table__free-proxy"]/div/table/tbody/tr')
    print(len(trs))

    for tr in trs:
        # tr 类型是 <class 'requests_html.Element'>

        # 结果还是 list，取第1个元素
        ip = tr.xpath('//td[1]/text()')[0]
        port = tr.xpath('//td[2]/text()')[0]
        position = tr.xpath('//td[5]/text()')[0]
        res_speed = tr.xpath('//td[6]/text()')[0]
        last_verify = tr.xpath('//td[7]/text()')[0]

        proxy["http"] = f"http://{ip}:{port}/"
        proxy["https"] = f"http://{ip}:{port}/"
        proxy["position"] = position
        proxy["res_speed"] = res_speed
        proxy["last_verify"] = last_verify
        # print(proxy)

        proxy_list.append(proxy)
    time.sleep(2)
    return proxy_list


def get_proxy_requests_regex():
    for url in proxy_urls:
        print(url)
        response = requests.get(url, headers=headers)
        html = response.text

        regex_fps = r"fpsList = \[([\s\S]*?)\]"

        # 正则匹配的结果类型是 list， 只含1个元素
        # 从 list 中取这个唯一元素，类型是 str
        fpsList = re.findall(regex_fps, html)
        if len(fpsList) == 0: exit()

        # re.findall 第1个参数是规则，第2个参数是字符串
        # 得到的结果应该是 字符串 list，每个'' 包括的{} 是一组，这样才能通过 json 转换成 字典
        # 所以要依据这个目的来设计正则匹配的规则
        regex_fp = r"(?={)([\s\S]*?)(?<=})"
        fps = re.findall(regex_fp, fpsList[0])
        print(fps)

        for fp in fps:
            proxy = json.loads(fp)
            proxy_list.append(proxy)

        return proxy_list


print(get_proxy_requests_regex())
