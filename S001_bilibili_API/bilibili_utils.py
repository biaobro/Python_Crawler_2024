# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : bilibili_utils.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/27 11:10
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/27 11:10 
@Version            : 1.0
@Description        : None
"""
import random
import math
import time

def toString(number, base):
    # 第1个参数是需要转换的数字
    # 第2个参数是需要转换的进制
    # 2个参数都应该是十进制数字类型，应该加上合法性判断
    base_str = {
        16: '0123456789abcdef',
        36: '0123456789abcdefghijklmnopqrstuvwxyz'
    }
    t_str = base_str[base]
    if number == 0:
        return '0'

    t_number = []
    while number != 0:
        # divmod 函数返回商 和 余数
        number, i = divmod(number, base)
        t_number.append(t_str[i])

    result = ''.join(reversed(t_number))

    # 转换成大写
    return result.upper()


def get_b_lsid():
    # generate random str
    t = ""

    # loop 8 times
    for n in range(8):
        r = random.random()
        t += toString(math.ceil(16 * r), 16)

    timestamp_13bits = int(round(time.time() * 1000))
    b_lsid = t + '_' + toString(timestamp_13bits, 16)
    return b_lsid


# "DF8528E5-B2F6-1BC6-B325-85A7104F69284 03611 infoc"
# 在 uuid 后面又补了2部分 时间戳计算 以及 infoc
def get_uuid():
    import uuid
    # uuid 也提供不同机制，4是基于随机数
    # 3 是手动指定命名空间 和 字符串
    # 1 是基于MAC和时间戳
    # js 源代码是 随机数 + 时间戳
    uuid = str(uuid.uuid4()).upper()
    timestamp_13bits = int(round(time.time() * 1000))
    suffix = str(timestamp_13bits % 100000) + 'infoc'
    return uuid + suffix