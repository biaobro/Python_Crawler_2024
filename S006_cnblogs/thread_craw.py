# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : thread.py
@Project            : S006_cnblogs
@CreateTime         : 2023/1/26 16:44
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/26 16:44 
@Version            : 1.0
@Description        : None
"""
import cnblogs_utils
import threading
import time


def single_thread_craw():
    print("single thread start")
    for url in cnblogs_utils.urls:
        cnblogs_utils.craw(url)
    print("single thread end")


def multi_thread_craw():
    print("multi thread start")
    threads = []
    for url in cnblogs_utils.urls:
        threads.append(threading.Thread(target=cnblogs_utils.craw, args=(url,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("multi thread end")


if __name__ == '__main__':
    start = time.time()
    single_thread_craw()
    end = time.time()
    print("single thread cost : ", end - start, "seconds")

    start = time.time()
    multi_thread_craw()
    end = time.time()
    print("multi thread cost : ", end - start, "seconds")
