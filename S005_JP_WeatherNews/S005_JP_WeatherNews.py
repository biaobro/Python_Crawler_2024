# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : S005_JP_WeatherNews.py
@Project            : S005_JP_WeatherNews
@CreateTime         : 2024/6/22 12:23
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/22 12:23 
@Version            : 1.0
@Description         : 注意异步调用的用法，通过 async 定义函数，在函数内部调用 await
                        然后又通过 assesion 调用
"""

import requests
from requests_html import AsyncHTMLSession

URL = 'https://weathernews.jp/wnl/timetable.html'


# URL = 'https://www.baidu.com'

def wait_render():
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get(URL)
        await r.html.arender(wait=5, sleep=5)
        return r

    r = assesion.run(process)[0]
    print(r.html)


def screenshot():
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get(URL)
        await r.html.arender(keep_page=True)
        await r.html.page.screenshot({'path': './ss.png'})
        return r

    r = assesion.run(process)[0]
    print(r.html)


def fullpage_screenshot():
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get(URL)
        await r.html.arender(keep_page=True)
        await r.html.page.screenshot({'path': './ss_fullpage.png', 'fullPage': True})
        return r

    r = assesion.run(process)[0]
    print(r.html)


def clip_screenshot():
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get(URL)
        clip = await r.html.arender(
            keep_page=True,
            script=(
                '''() => {
                    const rect = document.getElementById('main').getBoundingClientRect();
                    return {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height
                    };
                }'''
            ),
        )
        await r.html.page.screenshot({'path': './ss_clip.png', 'clip': clip})
        return r

    r = assesion.run(process)[0]
    print(r.html)


# execute_js 的效果不是很确认，失败的几率很高
def execute_js():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Content-Type': 'text/plain',
    }
    assesion = AsyncHTMLSession()

    async def process():
        r = await assesion.get(URL, headers=headers)
        await r.html.arender(
            keep_page=True,
        )
        main = await r.html.page.evaluate('document.querySelector("#main").clientHeight')
        print("main", main)
        # #sub > section.box.pb0
        topic = await r.html.page.evaluate('document.querySelector("#sub > section.box.pb0").clientHeight')
        print("topic", topic)
        return r

    r = assesion.run(process)[0]
    print(r.html)


if __name__ == "__main__":
    execute_js()
