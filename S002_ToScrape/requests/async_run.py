# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : async_run.py
@Project            : S002_ToScrape
@CreateTime         : 2024/7/29 00:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/7/29 00:03 
@Version            : 1.0
@Description        : None
"""
import asyncio
import aiohttp
import csv
import json
import time

from bs4 import BeautifulSoup


async def save_product(book_name, product_info):
    json_file_name = book_name.replace(' ', '_')
    with open(f'data/{json_file_name}.json', 'w') as book_file:
        json.dump(product_info, book_file)


async def scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body, 'html.parser')
            book_name = soup.select_one('.product_main').h1.text
            rows = soup.select('.table.table-striped tr')
            product_info = {row.th.text: row.td.text for row in rows}
            await save_product(book_name, product_info)


async def main():
    start_time = time.time()

    tasks = []
    with open('../extractToExcel/books.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            url = 'https://books.toscrape.com/catalogue/' + csv_row['link']
            task = asyncio.create_task(scrape(url))
            tasks.append(task)

    print('Saving the output of extracted information')
    await asyncio.gather(*tasks)

    time_diff = time.time() - start_time
    print(f'Scraping time : %.2f seconds. ' % time_diff)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
