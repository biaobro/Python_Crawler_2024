# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : sync_run.py
@Project            : S002_ToScrape
@CreateTime         : 2024/7/28 23:42
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/7/28 23:42 
@Version            : 1.0
@Description        : None
"""
import csv
import json
import time

import requests
from bs4 import BeautifulSoup


def save_product(book_name, product_info):
    json_file_name = book_name.replace(' ', '_')
    # 文件夹必须提前创建，否则报错
    with open(f'data/{json_file_name}.json', 'w') as book_file:
        json.dump(product_info, book_file)


def scrape(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    book_name = soup.select_one('.product_main').h1.text
    rows = soup.select('.table.table-striped tr')
    product_info = {row.th.text: row.td.text for row in rows}
    save_product(book_name, product_info)


def main():
    start_time = time.time()

    print('Saving the output of extracted information')
    with open('../books.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            url = 'https://books.toscrape.com/catalogue/' + csv_row['link']
            scrape(url)

    time_diff = time.time() - start_time
    print(f'Scraping time : %.2f seconds. ' % time_diff)


if __name__ == '__main__':
    main()
