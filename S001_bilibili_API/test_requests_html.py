# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : test_requests_html.py
@Project            : Crawler_2023
@CreateTime         : 2023/1/19 15:53
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/19 15:53 
@Version            : 1.0
@Description        : None
"""


from requests_html import AsyncHTMLSession
def wait_render():
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get("https://www.kuaidaili.com/free/inha/1")
        await r.html.arender(wait=5, sleep=5)
        return r

    r = assesion.run(process)[0]
    print(r.html)


if __name__ == "__main__":
    wait_render()

    



