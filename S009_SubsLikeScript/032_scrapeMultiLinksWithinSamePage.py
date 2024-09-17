# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 032_scrapeMultiLinksWithinSamePage.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/17 17:01
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/17 17:01 
@Version            : 1.0
@Description        : None
"""
import requests
from bs4 import BeautifulSoup

root = "https://subslikescript.com"
website = f"{root}/movies"
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

box = soup.find('article', class_='main-article')

links = []
for link in box.find_all('a'):
    links.append(link['href'])

    # print(links)
    website = root + link['href']
    result = requests.get(website)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    box = soup.find('article', class_='main-article')

    # 如果只想得到tag中包含的文本内容,那么可以用 get_text() 方法,
    # 这个方法获取到tag中包含的所有内容包括子孙tag中的内容,并将结果作为Unicode字符串返回:
    title = box.find('h1').get_text()
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')

    with open(f'./scripts/{title}.txt', 'w') as f:
        f.write(transcript)

    print("done on page : " + website)

