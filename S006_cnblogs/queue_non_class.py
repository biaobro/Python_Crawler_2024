# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : queue_non_class.py
@Project            : S006_cnblogs
@CreateTime         : 2023/1/26 18:33
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/26 18:33 
@Version            : 1.0
@Description        : None
"""
import queue
from datetime import datetime
import cnblogs_utils
import time
import random
import threading


def do_craw(url_queue: queue.Queue, html_queue: queue.Queue):
    while url_queue.not_empty:
        url = url_queue.get()
        html = cnblogs_utils.craw(url)
        html_queue.put(html)
        print(threading.current_thread().name, f"craw {url}",
              "url_queue.size = ", url_queue.qsize())
        time.sleep(random.randint(1, 2))
        url_queue.task_done()


def do_parse(html_queue: queue.Queue, fout):
    while html_queue.not_empty:
        html = html_queue.get()
        results = cnblogs_utils.parse(html)
        for result in results:
            fout.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + ',' + str(result) + '\n')
        print(threading.current_thread().name, f"results.size", len(results),
              "html_queue.size = ", html_queue.qsize())
        time.sleep(random.randint(1, 2))
        html_queue.task_done()


if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()

    for url in cnblogs_utils.urls:
        url_queue.put(url)

    # 创建线程列表
    thread_list = []

    fout = open("./data.txt", "w", encoding='utf-8')

    craw_thread = threading.Thread(target=do_craw, args=(url_queue, html_queue), name=f"craw")
    thread_list.append(craw_thread)

    parse_thread = threading.Thread(target=do_parse, args=(html_queue, fout), name=f"parse")
    thread_list.append(parse_thread)

    for t in thread_list:
        # 将每个进程设置为守护进程，效果是主进程退出后，不等子进程执行完也退出
        # 进程守护文章：
        t.daemon = True
        t.start()
    # 当主线程等待，所有的队列为空的时候才能退出
    url_queue.join()
    html_queue.join()



    # for idx in range(10):
    #     t = threading.Thread(target=do_craw, args=(url_queue, html_queue), name=f"craw{idx}")
    #     t.start()
    #
    # fout = open("./data.txt", "w", encoding='utf-8')
    # for idx in range(10):
    #     t = threading.Thread(target=do_parse, args=(html_queue, fout), name=f"parse{idx}")
    #     t.start()


    # 观察可以发现，craw 要比parse 耗时，同样的 queue 大小，html_queue 会经常处于空状态
