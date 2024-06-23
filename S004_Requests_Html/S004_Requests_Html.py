# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : S004_Requests_Html.py
@Project            : S004_Requests_Html
@CreateTime         : 2024/6/23 15:37
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/23 15:37 
@Version            : 1.0
@Description         : A simple demo to show how request-html
                    module be used to crawl javascript rendered page
@Video Address      : https://www.youtube.com/watch?v=-PmNcIX9En4
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup

url = "https://react-amazon-bestsellers-books-dy.netlify.app/"

session = HTMLSession()
resp = session.get(url)
resp.html.render()

# print(resp.html)

soup = BeautifulSoup(resp.html.html, 'html.parser')

books = soup.find_all('article', class_='book')

for book in books:
    title = book.find('h2').text
    print(title)