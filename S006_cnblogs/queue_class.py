# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : queue_class.py
@Project            : S006_cnblogs
@CreateTime         : 2024/6/29 21:14
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/29 21:14 
@Version            : 1.0
@Description         : None
"""

import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from multiprocessing.dummy import Pool
import json
import time


class Qsbk(object):
    """
    主要类，用来实现主要模型
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        }
        # 实例化三个队列，用来存放内容
        # 这时线程是安全的
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_total_url(self):
        """获取所有页面的url,并加入队列"""

        urls = [f"https://www.cnblogs.com/#p{page}" for page in range(1, 50 + 1)]

        # 将url添加到队列中
        for url in urls:
            self.url_queue.put(url)

    def get_response_html(self):
        """获取响应的html"""
        while self.url_queue.not_empty:
            # 判断非空，为空的时候结束循环

            # 从队列中取出一个url
            url = self.url_queue.get()
            print("parse url:", url)

            # 获取response
            resp = requests.get(url, headers=self.headers, timeout=1)

            # 将添加到html_queue
            self.html_queue.put(resp.text)

            """
            表明先前排队的任务已经完成，
            由队列使用者在线程中使用。
            对于用于获取任务的每个get()，随后对task_done()的调用告诉队列该处理任务完成了
            如果join()当前处于阻塞状态，则将在处理完所有项目后恢复。
            """
            # task_done的时候，队列计数减一
            self.url_queue.task_done()

    def get_content(self):
        """
        返回content_list
        获取内容：标题和连接
        """
        while self.html_queue.not_empty:
            # 从html_queue队列中获取单页的lxml化的html
            html = self.html_queue.get()

            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all("a", class_="post-item-title")

            # 创建一个content_list存放当前页下信息
            content_list = [(link["href"], link.get_text()) for link in links]

            # 将获得到的单页content_list放入content_queue中
            self.content_queue.put(content_list)

            # task_done的时候，队列计数减一
            self.html_queue.task_done()

    def save_content_to_file(self):
        """
        保存文件为json
        """
        while self.content_queue.not_empty:
            content_list = self.content_queue.get()
            with open("./data.json", 'a', encoding='utf8') as f:
                f.write(json.dumps(content_list, ensure_ascii=False, indent=2)[:-1] + ',')
                print("写入完成")
            # task_done的时候，队列计数减一
            self.content_queue.task_done()

    def run(self):
        """
        实现主要逻辑
        """
        start_ = time.time()

        # 创建线程列表
        thread_list = []

        # 创建获取total_url的线程
        url_thread = Thread(target=self.get_total_url)
        # 添加url_thread到thread_list中
        thread_list.append(url_thread)

        # 创建获取response_html的线程
        html_thread = Thread(target=self.get_response_html)
        # 添加html_thread到thread_list中
        thread_list.append(html_thread)

        # 创建获取content的线程
        content_thread = Thread(target=self.get_content)
        # 添加content_thread到thread_list中
        thread_list.append(content_thread)

        # 创建保存content的线程
        savefile_thread = Thread(target=self.save_content_to_file)
        # 添加到thread_list
        thread_list.append(savefile_thread)

        # 方式一
        # for t in thread_list:
        #     # 将每个进程设置为守护进程，效果是主进程退出后，不等子进程执行完也退出
        #     # 进程守护文章：
        #     t.setDaemon(True)
        #     t.start()
        # # 当主线程等待，所有的队列为空的时候才能退出
        # self.url_queue.join()
        # self.html_queue.join()
        # self.content_queue.join()

        # 方式二
        def process_thread(t):
            # 设置守护进程：https://www.cnblogs.com/nuochengze/p/12882349.html
            t.daemon = True
            t.start()

        pool = Pool(20)
        pool.map(process_thread, thread_list)

        # 当主线程等待，所有的队列为空的时候才能退出
        self.url_queue.join()
        self.html_queue.join()
        self.content_queue.join()

        ends_ = time.time()

        print("运行时间：", ends_ - start_)


if __name__ == '__main__':
    obj = Qsbk()
    obj.run()
