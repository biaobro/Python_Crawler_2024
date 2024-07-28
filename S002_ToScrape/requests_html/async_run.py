# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : async_run.py
@Project            : S002_ToScrape
@CreateTime         : 2024/6/16 23:43
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/16 23:43 
@Version            : 1.0
@Description         : None
"""
from requests_html import AsyncHTMLSession
import asyncio
import time

urls = []
for x in range(1, 2):
    urls.append(f'http://books.toscrape.com/catalogue/page-{x}.html')
print(len(urls))


async def work(s, url):
    r = await s.get(url)
    products = []
    desc = r.html.find('article.product_pod')
    for item in desc:
        product = {
            'a': item.find('a', first=True).attrs['href'],
            'title': item.find('h3 a[title]', first=True).text,
            'price': item.find('p.price_color', first=True).text,
        }
        products.append(product)
    return products


async def main(urls):
    s = AsyncHTMLSession()
    tasks = (work(s, url) for url in urls)
    return await asyncio.gather(*tasks)


start = time.perf_counter()
res = asyncio.run(main(urls))
print(res)
fin = time.perf_counter() - start
print(fin)
