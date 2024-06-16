# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : proxy_myserver_tinyproxy.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/20 21:54
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/20 21:54 
@Version            : 1.0
@Description        : None
"""

import requests
import random

# 位于阿里云和腾讯云服务器上的代理，通过 TinyProxy 支持
# 能够正常使用的前提，TinyProxy 服务正常，对应端口被放行
proxy_list = [
    {"http": "http://121.43.130.188:8765/", "https": "http://121.43.130.188:8765/", "name": "AliYun_Proxy"},
    {"http": "http://101.42.117.166:8910/", "https": "http://101.42.117.166:8910/", "name": "TecentCloud_Proxy"},
]

url1 = "http://httpbin.org/ip"
url2 = 'http://www.baidu.com'
proxy = random.choice(proxy_list)

headers = {
    'user-agent': 'Safari/537.36 OPR/26.0.1656.60'
}

response = requests.get(url1, proxies=proxy, headers=headers)
print(proxy['name'], response.text)

print(response.request.headers)
