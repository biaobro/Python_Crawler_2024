# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : cnblogs_utils.py
@Project            : S006_cnblogs
@CreateTime         : 2023/1/26 16:39
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/26 16:39 
@Version            : 1.0
@Description        : None
"""
import requests
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1, 50 + 1)
]

# print(urls)

def craw(url):
    r = requests.get(url)
    return r.text


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]


if __name__ == '__main__':
    for result in parse(craw(urls[0])):
        print(result)
