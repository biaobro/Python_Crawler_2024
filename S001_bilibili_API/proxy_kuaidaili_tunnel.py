# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : proxy_kuaidaili_tunnel.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/20 17:40
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/20 17:40 
@Version            : 1.0
@Description        : 这是 kuaidaili 提供的隧道代理 示例代码，免费试用时长只有6小时
"""

import requests

# 隧道域名:端口号
tunnel = "h876.kdltpspro.com:15818"

# 用户名密码方式
username = "t11845424163661"
password = "pv6mpy38"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

# 白名单方式（需提前设置白名单）
# proxies = {
#     "http": "http://%(proxy)s/" % {"proxy": tunnel},
#     "https": "http://%(proxy)s/" % {"proxy": tunnel}
# }

# 要访问的目标网页
target_url = "https://dev.kdlapi.com/testproxy"

# 使用隧道域名发送请求
response = requests.get(target_url, proxies=proxies)

# 获取页面内容
if response.status_code == 200:
    print(response.text)  # 请勿使用keep-alive复用连接(会导致隧道不能切换IP)
