"""
# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
#File               : book.py
#Project            : 001-Crawler
#CreateTime         : 2022/1/31 12:00
#Author             : biaobro
#Software           : PyCharm
#Last Modify Time   : 2022/1/31 12:00
#Version            : 1.0
#Description        :
    @tag: 图书标签
    @根据提供的标签，得到书ID，书名，图片链接，出版信息，评分，评价人数
    @用到了 Beautifulsoup 的 select 方法
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
import re
import itertools

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

tag = "武术"
url_base = "https://book.douban.com/tag/" + quote(tag)
# url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=1000&type=T"
# 豆瓣的返回内容中，没有数量，没有办法提前预知结果数量
book_count = 0

if __name__ == '__main__':
    # itertools.count 生成无限递归序列
    for i in itertools.count():
        print(i)

        # type = 综合排序
        # type = R 按出版日期排序
        # type = S 按评价排序
        url = url_base + "?start={}&type=S".format(i * 20)
        print(url)

        try:
            html = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            break
        # print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')

        # subject-item 是每个 li 标签的 class 属性
        books = soup.select('.subject-item')
        if len(books) == 0:
            print("{} items of {} has been grabbed".format(book_count, tag))
            break

        for book in books:
            book_count += 1
            # 获取ID
            try:
                # li 标签下的第1个 div 标签 class 为 pic
                onclick = book.select('.pic a')[0]['onclick']
                # print(onclick)
            except Exception as e:
                print(e, "error while get subject_id")
            else:
                # 从onclick里得到subject_id有2种方法
                # 方法1: json解析 测试后废弃，因为onclick的内容不是标准的json格式
                # 标准json格式需要key和value都用双引号括起来，而不是单引号
                # start = onclick.find('{')
                # end = onclick.find('}')
                # content = json.loads(onclick[start, end])
                # subject_id = content['subject_id']

                # 方法2：正则表达式
                regex_id = r"subject_id:'(\d+)"
                subject_id = re.findall(regex_id, onclick)[0]
                print('book id : {}'.format(subject_id))

            try:
                # 获取书面图片链接
                img_link = book.select('.pic img')[0]['src']
                print('book cover : {}'.format(img_link))
            except Exception as e:
                print(e, "error while get cover")

            try:
                # 获取书名
                # info 是 li 标签下的第2个 div 标签
                title = book.select('.info h2 a')[0]['title']
                print('book title : {}'.format(title))
            except Exception as e:
                print(e, "error while get title")

            try:
                # 获取出版信息
                # pub 可以用/做split，得到作者，出版社，出版日期，价格
                pub = book.select('.info .pub')[0].text.strip().replace(" ", '').replace("\n", ' ')
                print('book pub : {}'.format(pub))
            except Exception as e:
                print(e, "error while get publish info")

            try:
                # 获取评分
                rating_nums = book.select('.star.clearfix .rating_nums')[0].text
                print('book rating : {}'.format(rating_nums))
            except Exception as e:
                # 有些书 没有人评价 或者 评价人数少于10人，就没有评分
                # print(e, "error while get rating")
                print('no rating. ')

            # print("catch people start.............................")

            try:
                # 获取评价人数
                appraiser = book.select('.info .star.clearfix .pl')[0].text.strip().replace(" ", '').replace("\n", ' ')
                # 正则匹配全部数字，注意匹配结果是个列表
                regex_num = r"\d+"
                print(re.findall(regex_num, appraiser)[0])
                # print('book appraiser : {}'.format(appraiser))
            except Exception as e:
                print(e, "error while get people_nums")
