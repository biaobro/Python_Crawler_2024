# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 026_exportToTxt.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/17 16:52
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/17 16:52 
@Version            : 1.0
@Description        : None
"""
import requests
from bs4 import BeautifulSoup

website = "https://subslikescript.com/movie/Titanic-120338"
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

box = soup.find('article', class_='main-article')

# 如果只想得到tag中包含的文本内容,那么可以用 get_text() 方法,
# 这个方法获取到tag中包含的所有内容包括子孙tag中的内容,并将结果作为Unicode字符串返回:
title = box.find('h1').get_text()
transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')

with open(f'{title}.txt', 'w') as f:
    f.write(transcript)
