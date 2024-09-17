# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 024_getHtml.py
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
print(soup.prettify())
