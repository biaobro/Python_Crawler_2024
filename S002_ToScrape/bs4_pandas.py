# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : bs4_pandas.py
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

while True:

    books = []
    for page in range(1,2):

        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        ol = soup.find('ol')
        articles = ol.find_all('article', class_='product_pod')

        for article in articles:
            link = article.find('a').attrs['href']
            image = article.find('img')
            title = image.attrs['alt']
            star = article.find('p')['class'][1]
            price = float(article.find('p', class_='price_color').text[1:])

            books.append([link, title, price, star])

        print(f"{url} scrape done!")

    # print(books)
    df = pd.DataFrame(books, columns=['link', 'title', 'price', 'star'])
    df.to_csv('books.csv', index=False)

    if len(df) > 20:
        smt = smtplib.SMTP('smtp.sina.com',25)

        srcAddr = "biaobro@sina.com"
        authCode = '454c3e4b484b6222'
        targetAddrs = ["weibiao.wb@alibaba-inc.com"]

        # Add the From: and To: headers at the start!
        subject = f'Subject: Book Notifier\n\nHi There, book count has exceed to {len(df)}'
        lines = [f"From: {srcAddr}", f"To: {', '.join(targetAddrs)}", subject]
        msg = "\r\n".join(lines)

        # sina邮箱需要用第三方授权码，直接登录的密码不行
        smt.login(srcAddr,authCode)

        # 可以打印出和SMTP服务器交互的所有信息
        smt.set_debuglevel(1)

        smt.sendmail(srcAddr, targetAddrs, msg)
        smt.quit()
    break
    time.sleep(24*60*60)
