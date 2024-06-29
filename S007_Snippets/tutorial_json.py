# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : tutorial_json.py
@Project            : S007_BeautifulSoup
@CreateTime         : 2024/6/30 00:14
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/30 00:14 
@Version            : 1.0
@Description        : None
"""
import json
from urllib.request import urlopen


def fun1():
    # json.load 得到的就已经是 字典了
    # json.load 可以读取文件 得到 字典
    # json.loads 只能读取json字符串，得到 字典
    with open('states.json') as f:
        data = json.load(f)

    print(type(data))

    for state in data['states']:
        del state['area_codes']

    # json.dump 和 json.dumps 也是相同的道理
    with open('states_new.json', 'w') as f:
        json.dump(data, f, indent=2)


def fun2():
    with urlopen("https://edge-mcdn.secure.yahoo.com/ybar/exp.json") as resp:
        src = resp.read()

    data = json.loads(src)

    # print(json.dumps(data, indent=2))
    print(data)

    exp_data = dict()

    for item in data['expList']:
        name = item['name']
        timeout = item['timeout']

        exp_data[name] = timeout

    print(exp_data)

fun2()
