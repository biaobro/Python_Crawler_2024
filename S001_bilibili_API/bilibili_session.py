# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : bilibili_session.py
@Project            : 001-Crawler
@CreateTime         : 2023/1/20 10:59
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/1/20 10:59 
@Version            : 1.0
@Description        : None
@why why why????
"""
import requests
import re
import json
import random
import math
import time
from urllib.parse import urlencode
from fake_useragent import UserAgent
import sys
from bilibili_utils import get_b_lsid, get_uuid

# from get_proxy import get_proxy

proxy_list = [
    # {"http": "http://121.43.130.188:8765/", "https": "http://121.43.130.188:8765/", "position": "A_Tiny_Proxy"},
    {"http": "http://101.42.117.166:8910/", "https": "http://101.42.117.166:8910/", "position": "T_Tiny_Proxy"},
    # {"http": "", "https": "", "position": "L_N_Proxy"},
    # {"http": "socks5://101.42.117.166:8911/", "https": "socks5://101.42.117.166:8911/", "position": "T_Gost_Proxy"},
    # {"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808", "position": "W_VPN_Proxy"},
    # {"http": "http://127.0.0.1:11457", "https": "http://127.0.0.1:11457", "position": "W_Fiddler_Proxy"},
]

print("There are {} proxies".format(len(proxy_list)))

# 得到本机公网IP，从自己的 proxy_list 移除
# 为了用1套代码 视频阿里云 和 腾讯云 上的2个机器
# 最早效果就是要么走代理到对方，要么不走代理。不会走到自己代理自己
response = requests.get('http://myip.ipip.net', timeout=5)
regex = r'IP：(\d+.\d+.\d+.\d+)'
public_ip = re.findall(regex, response.text)[0]
print('public_ip of local machine {} will be removed from proxy_list'.format(public_ip))

for proxy, i in zip(proxy_list, range(len(proxy_list))):
    if public_ip in proxy['http']:
        del proxy_list[i]

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# 固定的 video_list 参数，字典列表
video_list = [
    {'url': 'https://www.bilibili.com/video/BV1qv4y1C76s/'},
    # {'url': 'https://www.bilibili.com/video/BV1B3411X7QJ/'},
    # {'url': 'https://www.bilibili.com/video/BV1VM411y7oS/'},
    # {'url': 'https://www.bilibili.com/video/BV1v14y137ke/'},
    # {'url': 'https://www.bilibili.com/video/BV1Vg411x7AV/'},
    # {'url': 'https://www.bilibili.com/video/BV1XY41127G5/'},
    # {'url': 'https://www.bilibili.com/video/BV1BG4y1m7Cp/'},
    # {'url': 'https://www.bilibili.com/video/BV1cd4y1h7vk/'},
    # {'url': 'https://www.bilibili.com/video/BV1kK41117o7/'},
    # {'url': 'https://www.bilibili.com/video/BV1Y24y1U7jP/'},
    # {'url': 'https://www.bilibili.com/video/BV1vY41127Zy/'},
    # {'url': 'https://www.bilibili.com/video/BV1AG4y1m7Kj/'},
]

failure_level = ['normal', 'bad', 'serious', 'severe']
# 判断是否在通过 Python xxx.py 执行时有输入参数，如果有，就用输入的参数执行，否则用上面写死的
# 参数为视频的url 地址，多个地址之间通过 , 分隔
url_params = []
if len(sys.argv) > 1:
    # 如果有输入，就清空固定参数
    video_list.clear()
    # 获取输入参数，得到列表
    url_params = sys.argv[1].split(',')
    # 将新的参数添加到 video_list(字典)
    for url in url_params:
        video_list.append({'url': url})

count = 1
while count < 10:
    # 如果video 请求失败次数过多，就从 video_list 中移除
    # video_list 如果元素都被移除，就不再循环
    if len(video_list) == 0:
        print("no target video in video_list, program will be ended.")
        exit()
    try:
        for video in video_list[:]:
            session = requests.Session()
            # 循环
            # proxy = random.choice(proxy_list)
            # 轮流
            # proxy = proxy_list[count % len(proxy_list)]
            # print('{} : session started with 【{}】'.format(time.strftime("%Y-%m-%d %H:%M:%S"), proxy['position']))
            # session.proxies = proxy
            session.headers.update({'user-agent': UserAgent().random})

            # 因为使用 session，所以 headers 只需要传递1次
            # 1st request to get 2 cookies : buvid3, b_nut
            response = session.get(url=video['url'], headers=headers)

            # 正则提取 视频播放量
            # 每次都获取展示播放量，以确认成功率
            # re.findall 得到的是1个列表
            regex_result = re.findall(r'view-text.*?>(\d+?)<', response.text)
            if len(regex_result) == 0:
                print('Error: Count info not been retrieved. ')
                raise Exception("HtmlCodeException@Count")
            video['current_count'] = regex_result[0]

            # 第一次请求后，保存视频名称，初始播放量
            aid, cid = '', ''
            if count == 1:
                # 初始化2个控制参数，1个是连续失败次数，1个是播放间隔（也就是接口请求间隔）
                video['failure_count'] = 0
                video['interval'] = 60
                video['failure_level'] = ''
                video['delay_flag'] = False

                # 每个视频的 aid,cid 不变，只读取1次，保存即可
                regex_result = re.findall(r'__INITIAL_STATE__=([\s\S]*?)\"upData', response.text)
                if len(regex_result) == 0:
                    print('Error: aid & cid & duration info not been retrieved. ')
                    raise Exception("HtmlCodeException@aid&cid&duration")

                # 因为正则匹配的原因，data_list[0] 末尾带了1个逗号 , 通过切片将其去掉
                # 然后再补1个 } 以便进行接下来的 json 转换
                data_str = regex_result[0][:-1] + "}"

                # 将 字符串 转换成 字典
                data_dict = json.loads(data_str)

                video['aid'] = str(data_dict['aid'])
                video['cid'] = str(data_dict['videoData']['cid'])
                video['duration'] = str(data_dict['videoData']['duration'])

                video['init_count'] = int(video['current_count'])

                # 正则提取视频名称
                regex_result = re.findall(r'<title data-vue-meta=\"true\">(.*?)_哔哩哔哩_bilibili<\/title>',
                                          response.text)
                if len(regex_result) == 0:
                    print('Error: Name info not been retrieved. ')
                    raise Exception("HtmlCodeException@Name")
                video['name'] = regex_result[0]

            print('{:22}Video name : 【{}】 '.format('', video['name']))
            print('{:22}initial count is : 【{}】, current count is : 【{}】'.format('', video['init_count'],
                                                                                 video['current_count']))

            # Todo : 应该有这样的逻辑，如果连续N次发送请求，播放数量都没有变化
            # Todo : 那就加大发送间隔，或者停止发送，或者其他逻辑？ 需要增加线程，进程处理，不能再在1个for循环里搞了
            # for 循环里做的延迟 只能针对全部，不能针对某个 url 地址
            # 监测是否刷新成功，第1次无需执行，从 count = 2 时开始
            # count_current 比 count_last 多 1，表示成功
            # count_current 和 count_last 相等，表示失败
            if count > 1:
                # 如果count没有变化，失败次数加1
                if int(video['current_count']) - int(video['last_count']) == 0:
                    video['failure_count'] = int(video['failure_count']) + 1

                # 如果count发生变化，失败次数减1
                # 如果 failure_count 已经是0了，就不再扣减
                # current_count 和 last_count 有可能相差2，请求2次才会变化，所以用了 >=1
                elif (int(video['failure_count']) > 0) and (
                        int(video['current_count']) - int(video['last_count']) >= 1):
                    video['failure_count'] = int(video['failure_count']) - 1
                print('{:22}failure count is : 【{}】'.format('', video['failure_count']))

                # 根据 failure_count 得到 failure_level, 以5个 failure_count 为单位
                video['failure_level'] = failure_level[math.floor(int(video['failure_count']) / 5)]
                print('{:22}failure level is : 【{}】'.format('', video['failure_level']))

                # 判断失效次数，以5为1个单位，调整 interval
                # 如何处理 failure_count 再降回正常值时的情况？
                # 'normal:<=5', '5<bad<=10', '10<serious<=15', '15<severe'
                if video['failure_level'] == 'bad' and not video['delay_flag']:
                    # 失败次数在 6-10 范围之间
                    video['interval'] = int(video['interval']) + 15
                    video['delay_flag'] = True
                elif video['failure_level'] == 'serious' and video['delay_flag']:
                    video['interval'] = int(video['interval']) + 30
                    video['delay_flag'] = False
                elif video['failure_level'] == 'severe':
                    # 剔除
                    video_list.remove(video)
                    print('{:22}too many failures. will be kicked out and no further progress .'.format(''))
                    continue
                print('{:22}request interval is : 【{}】'.format('', video['interval']))

            # 更新变量，将当前 count 保存为 count_last
            video['last_count'] = video['current_count']

            # insert 1 fix cookie
            session.cookies.set('CURRENT_FNVAL', '4048')

            # 2nd request to get 1 cookies : sid
            response = session.get(
                url='https://api.bilibili.com/x/player/v2?',
                params={
                    'aid': video['aid'],
                    'cid': video['cid']
                },
            )

            # retrieve the ip_info from server's response
            ip_location = response.json()['data']['ip_info']['province']
            print('{:22}ip_location been reported to server is : 【{}】'.format('', ip_location))

            # insert 2 cookies generate locally
            session.cookies.set('b_lsid', get_b_lsid())

            session.cookies.set('_uuid', get_uuid())

            # get b_4 from spi response
            response = session.get('https://api.bilibili.com/x/frontend/finger/spi')
            b_4 = response.json()['data']['b_4']
            # insert 1 cookie should be urlencode
            # session.cookies.set('buvid4', urlencode({'buvid4': b_4}).split('=')[1])
            session.cookies.set('buvid4', b_4)

            print('{:22}request will be sent 【{}】 times. expected count is 【{}】\n'.format('',
                                                                                          count,
                                                                                          video['init_count'] + count))

            url_h5 = 'https://api.bilibili.com/x/click-interface/click/web/h5'
            response = session.post(
                url=url_h5,
                params={
                    'aid': video['aid'],
                    'cid': video['cid'],
                    'part': '1',
                    'lv': '0',
                    'ftime': str(int(time.time()) * 1000),
                    'stime': str(int(time.time()) * 1000),
                    'type': '3',
                    'sub_type': '0',
                },
            )

            params_heartbeat = {
                'start_ts': str(int(time.time())),
                'aid': video['aid'],
                'cid': video['cid'],
                'type': '3',
                'sub_type': '0',
                'dt': '2',
                'play_type': '4',  # 0 是播放中 # 4是播放完成
                'realtime': video['duration'],
                'played_time': '-1',  # -1 对应播放完成
                'real_played_time': video['duration'],  # 会随着倍数速率变化
                'refer_url': '',  # 'https://space.bilibili.com/301311051',  # 可不写
                'quality': '0',
                'video_duration': video['duration'],  # 每个视频时长固定
                'last_play_progress_time': video['duration'],  # 随播放过程变化
                'max_play_progress_time': video['duration'],  # 如果是完整播放，这3个值应该一样
                'spmid': '333.788.0.0',  # 页面本身的参数
                'from_spmid': '',  # '333.999.0.0',  # 这个值和refer_url 是一一对应的
                'crsf': ''
            }

            # 播放过程中也会发出 heartbeat, 时间间隔多变 10s一次？
            # 播放完成后的 heartbeat
            # 好像发不发
            # url_heartbeat = 'https://api.bilibili.com/x/click-interface/web/heartbeat'
            # result = session.post(
            #     url=url_heartbeat,
            #     params=params_heartbeat,
            # )

            # check response
            print('{:22}'.format('', response.content))

            session.close()
            # time.sleep(int(video['interval']))
        time.sleep(60)
    except KeyboardInterrupt:
        print('KeyboardInterrupt been got. program will be existed. ')
        for video in video_list:
            print("""{} : 
                        initial count {}, 
                        sent requests {}, 
                        current count {},
                        success times {}, 
                        success rate  {:.2%} """.format(
                video['name'],
                video['init_count'],
                count,
                video['current_count'],
                int(video['current_count']) - int(video['init_count']),
                (int(video['current_count']) - int(video['init_count'])) / count
            )
            )
        exit()
    except Exception as e:
        print('Exception been got : ', repr(e))
        with open('error.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
    finally:

        count = count + 1
