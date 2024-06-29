# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : tutorial_beautifulsoup.py
@Project            : S007_Snippets
@CreateTime         : 2024/6/29 23:24
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/29 23:24 
@Version            : 1.0
@Description        : None
"""
from bs4 import BeautifulSoup
import requests
import csv

with open('demo.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# print(soup.prettify())

# 只返回第一个 div 目标
# match = soup.div

# 返回满足条件的第1个div
# match = soup.find('div', class_='footer')
# print(match.prettify())

# article = soup.find('div', class_='article')
# # print(article)

csv_file = open('tutorial.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary'])

# find_all 返回满足条件的全部 div
for article in soup.find_all('div', class_='article'):
    try:
        headline = article.h2.a.text
        print(headline)

        summary = article.p.text
        print(summary)
    except Exception as e:
        # raise e
        headline = ''
        summary = ''

    print()

    csv_writer.writerow([headline, summary])
csv_file.close()


