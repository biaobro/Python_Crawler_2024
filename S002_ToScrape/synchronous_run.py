# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : synchronous_run.py
@Project            : S002_ToScrape
@CreateTime         : 2024/6/16 23:36
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/16 23:36 
@Version            : 1.0
@Description         : None
"""
from requests_html import HTMLSession
import time

urls = []
for x in range(1,51):
    urls.append(f'http://books.toscrape.com/catalogue/page-{x}.html')
print(len(urls))

def work(url):
    r = s.get(url)
    products = []

    # find 的参数 标签名称.类型名称
    desc = r.html.find('article.product_pod')
    for item in desc:
        product = {
            # find 的参数 标签名称 子标签名称[子标签里的属性]
            'title': item.find('h3 a[title]', first=True).text,
            'price': item.find('p.price_color', first=True).text,
        }
        products.append(product)
    return products

def main(urls):
    for url in urls:
        print(work(url))
    return

s = HTMLSession()
start = time.perf_counter()
main(urls)
fin = time.perf_counter() - start
print(fin)

# 62.01709929696517
