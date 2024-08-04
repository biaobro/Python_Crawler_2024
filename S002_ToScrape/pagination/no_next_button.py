# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : no_next_button.py
@Project            : S002_ToScrape
@CreateTime         : 2024/8/4 16:05
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/8/4 16:05 
@Version            : 1.0
@Description        : None
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.gosc.pl/Kosciol'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
page_link_el = soup.select('.pgr span a')
print(len(page_link_el))
# do more with the first page

# make links for and process the remaining pages
for link_el in page_link_el:
    link = urljoin(url, link_el.get('href'))
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    print(response.url)


