# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : next_button.py
@Project            : S002_ToScrape
@CreateTime         : 2024/8/4 16:38
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/8/4 16:38 
@Version            : 1.0
@Description        : None
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    footer_element = soup.select_one('li.current')

    print(footer_element.text.strip())

    # pagination
    # css 选择器： 标签 -> CSS样式 -> 标签
    next_page_element = soup.select_one('li.next > a')
    if next_page_element:
        next_page_url = next_page_element.get('href')
        url = urljoin(url, next_page_url)
    else:
        break



