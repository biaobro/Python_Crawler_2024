# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : scrape.py
@Project            : S002_ToScrape
@CreateTime         : 2024/6/16 23:43
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/16 23:43
@Version            : 1.0
@Description         : None
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
import time


def get_data(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    ol = soup.find('ol')
    books = ol.find_all('article', class_='product_pod')

    data = []
    columns = ['link', 'title', 'price', 'star']

    for book in books:
        link = book.find('a').attrs['href']
        image = book.find('img')
        title = image.attrs['alt']
        star = book.find('p')['class'][1]
        price = float(book.find('p', class_='price_color').text[1:])

        data.append([link, title, price, star])

    print(f"{url} scrape done!")
    return data, columns


def export_data(data, columns):
    # columns = ['link', 'title', 'price', 'star']
    df = pd.DataFrame(data, columns=columns)
    df.to_excel('books.xlsx')
    df.to_csv('books.csv', index=False)


def mail_data(targetAddrs, subject):
    smt = smtplib.SMTP('smtp.sina.com', 25)

    srcAddr = "biaobro@sina.com"
    authCode = '454c3e4b484b6222'

    # Add the From: and To: headers at the start!
    subject = f'Subject: Book Notifier\n\nHi There, book count has exceed the limit!'
    lines = [f"From: {srcAddr}", f"To: {', '.join(targetAddrs)}", subject]
    msg = "\r\n".join(lines)

    # sina邮箱需要用第三方授权码，直接登录的密码不行
    smt.login(srcAddr, authCode)

    # 可以打印出和SMTP服务器交互的所有信息
    smt.set_debuglevel(1)

    smt.sendmail(srcAddr, targetAddrs, msg)
    smt.quit()


if __name__ == '__main__':
    for page in range(1, 2):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        data,cols = get_data(url)
        export_data(data,cols)
        mail_data(["weibiao.wb@alibaba-inc.com"], "Get out")

        time.sleep(60)
