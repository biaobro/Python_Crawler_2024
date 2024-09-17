# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 025_scrapeSinglePage.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/17 16:33
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/17 16:33 
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

title = box.find('h1').get_text()
print(title)

transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')
print(transcript)