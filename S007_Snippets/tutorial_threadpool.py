# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : tutorial_threadpool.py
@Project            : S007_BeautifulSoup
@CreateTime         : 2024/6/30 09:11
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/30 09:11 
@Version            : 1.0
@Description        : None
"""
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED
import time

def waste(n):
    print(f'{n} started!')
    time.sleep(n)
    print(f'{n} finished')
    return f'{n} return value'

threads = []
t = ThreadPoolExecutor(max_workers=3)
threads.extend(t.submit(waste, i) for i in range(10, 1, -1))

    # for thread in as_completed(threads, timeout=3):
    #     print(thread.result())

print(wait(threads, timeout=5, return_when=FIRST_COMPLETED))
print('program exist!')
