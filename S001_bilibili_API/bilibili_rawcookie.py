# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : bilibili_rawcookie.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/18 23:05
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/18 23:05 
@Version            : 1.0
@Description        : None
"""
import requests
import json
import re
from http.cookies import SimpleCookie
from requests.utils import dict_from_cookiejar
from urllib.parse import urlencode
import time
import random
import math
from fake_useragent import UserAgent

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def get_aid_cid_buvid3(url):
    print(url)

    result = requests.get(url, headers=headers)
    # 方式1
    # print(result.raw.headers.getlist('Set-Cookie'))

    # 方式2
    # if 'Set-Cookie' in result.headers:
    #     simple_cookie = SimpleCookie(result.headers['Set-Cookie'])
    #     for item in simple_cookie:
    #         # cook = cook + '; ' + item + "=" + simple_cookie[item].value
    #         print(item)
    # else:
    #     print(result.headers)

    # 方式3
    # to_set_cookie = dict_from_cookiejar(result.cookies)
    # print(to_set_cookie)

    # 方式4
    # print(result.cookies)
    cookies = result.cookies.get_dict()
    # print(cookies)
    buvid3 = cookies['buvid3']
    # print('buvid3', buvid3)

    # 从response headers 中得到 cookie
    # 从网页源代码中的得到 aid,cid
    # 这里要注意1点 从浏览器控制台看到的 result.text
    data_list = re.findall(r'__INITIAL_STATE__=([\s\S]*?)\"upData', result.text)

    # 因为正则匹配的原因，data_list[0] 末尾带了1个逗号 , 通过切片将其去掉
    # 然后再补1个 } 以便进行接下来的 json 转换
    data_str = data_list[0][:-1] + "}"
    # print(data_str)

    # 将 字符串 转换成 字典
    data_dict = json.loads(data_str)

    aid = str(data_dict['aid'])
    cid = str(data_dict['videoData']['cid'])

    # 得到说明：<span title=\"(.*?)\" class=\"view item\">
    # 得到数字：<span title=\".*?(\d+?)\" class=\"view item\">
    play_count_show = int(re.findall(r'view-text.*?>(\d+?)<', result.text)[0])

    # print('aid', aid)
    # print('cid', cid)

    return aid, cid, buvid3, play_count_show


def get_sid(aid, cid, buvid3):
    payload = {
        'aid': aid,
        'cid': cid
    }

    url = 'https://api.bilibili.com/x/player/wbi/v2?' + urlencode(payload)

    cookies = {
        'buvid3': buvid3,
        'b_nut': str(int(time.time()) * 1000),
        'CURRENT_FNVAL': '4048'
    }

    result = requests.get(url, cookies=cookies, headers=headers)

    cookies = result.cookies.get_dict()
    sid = cookies['sid']
    return sid


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


def get_spi(buvid3, sid, b_lsid, _uuid):
    url = 'https://api.bilibili.com/x/frontend/finger/spi'
    cookies = {
        'buvid3': buvid3,
        'b_nut': str(int(time.time()) * 1000),
        'CURRENT_FNVAL': '4048',
        'sid': sid,
        'b_lsid': b_lsid,
        '_uuid': _uuid
    }

    # 这里请求 headers 和全局 headers 的差异， accept-encoding 去掉了 br
    # 否则 服务端会返回 br 压缩格式的响应，而 requests 仅支持  'gzip' 压缩和 'deflate' 压缩类型
    # 所以2种解法，1种就是发起请求时就不带 br，这样服务端也就不会返回。 这里采用该方法
    # 另1种是安装 Brotli，if response.headers[ "Content-Encoding"] == 'br': resp_json = brotli.decompress(response.content)
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    result = requests.get(url, cookies=cookies, headers=headers)

    # bytes 类型
    # print(result.content)

    # str 类型
    # print(result.text)

    b_3 = result.json()['data']['b_3']
    b_4 = result.json()['data']['b_4']

    return b_3, b_4


def play(aid, cid, buvid3, sid, b_lsid, _uuid, buvid4):
    url = 'https://api.bilibili.com/x/click-interface/click/web/h5'
    headers = {
        'user-agent': UserAgent().random
    }

    payload = {
        'aid': aid,
        'cid': cid,
        'part': '1',
        'lv': '0',
        'ftime': str(int(time.time()) * 1000),
        'stime': str(int(time.time()) * 1000),
        'type': '3',
        'sub_type': '0',
    }
    cookies = {
        'buvid3': buvid3,
        'b_nut': str(int(time.time()) * 1000),
        'CURRENT_FNVAL': '4048',
        'sid': sid,
        'b_lsid': b_lsid,
        '_uuid': _uuid,
        'buvid4': buvid4
    }

    result = requests.post(url, headers=headers, cookies=cookies, data=payload)

    return result


if __name__ == '__main__':
    # url 要带上最后的/，不带的话返回的是 302 Redirect，拿不到cookie
    urls = [
        'https://www.bilibili.com/video/BV1qv4y1C76s/',
        # 'https://www.bilibili.com/video/BV1ud4y177TM/',
        # 'https://www.bilibili.com/video/BV1SA411f7he/',
        # 'https://www.bilibili.com/video/BV1v14y137ke/',
        # 'https://www.bilibili.com/video/BV1Bd4y1V7g3/'
    ]

    count = 1
    while count < 2:
        for i in range(1):
            aid, cid, buvid3, play_count_init = get_aid_cid_buvid3(urls[i])
            print('{} aid : {}, cid : {}, buvid3 : {}, play_count_show : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                    aid, cid, buvid3,
                                                                                    play_count_init))

            sid = get_sid(aid, cid, buvid3)
            print('{} sid : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), sid))

            b_lsid = get_b_lsid()
            print('{} b_lsid : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), b_lsid))

            _uuid = get_uuid()
            print('{} _uuid : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), _uuid))

            # b_3 实际没有使用
            b_3, b_4 = get_spi(buvid3, sid, b_lsid, _uuid)
            print('{} b_3 : {}, b_4 : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), b_3, b_4))

            buvid4 = urlencode({'buvid4': b_4}).split('=')[1]
            print('{} buvid4 : {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), buvid4))

            res = play(aid, cid, buvid3, sid, b_lsid, _uuid, buvid4)
            print("Response: ", res.text)

            if res.json()['code'] != 0:
                print('h5 play request failed.')
                raise Exception

            print('{:20}send play request {} times. play_count would be : {}.'.format('',
                                                                                      count,
                                                                                      play_count_init + count))
            print('{:20}random-ua : {}  \n'.format('', res.request.headers['user-agent']))
            time.sleep(5)

        count = count + 1
