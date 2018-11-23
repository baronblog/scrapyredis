# -*- coding: utf-8 -*-
import datetime
import requests
import time
import sched

from threading import Timer
from lxml import etree
from urllib.parse import unquote

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from proxyPool.dbManager.proxyDBManager import ProxyDBManager
from proxyPool.model.proxy import Proxy
from proxyPool.spiders.xiciSpider import XiciSpider

"""
    测试用例
@Author monkey
@Date 2017-12-3
"""

"""
# =======================================================================
# 测试用例1
# 从 url中切割非中文类型字符串
# =======================================================================
"""


def case_1():
    url = 'https://www.lagou.com/zhaopin/Python/'
    dirt = url.split('/')[-2]
    print('dirt value is === ' + dirt)


"""
# =======================================================================
# 测试用例2
# 从 url中切割中文类型字符串
# =======================================================================
"""


def case_2():
    urllist = [
        'https://www.lagou.com/zhaopin/C%23/',
        'https://www.lagou.com/zhaopin/meishushejishi%EF%BC%882D3D%EF%BC%89/',
    ]

    for url in urllist:
        dirt = unquote(url.split('/')[-2])
        print('dirt value is === ' + dirt)


"""
# =======================================================================
# 测试用例3
# 从 url中切割 number
# =======================================================================
"""


def case_3():
    url = 'https://www.lagou.com/zhaopin/Python/2/?filterOption=2'
    number = url.split('/')[-2]
    print(number)


"""
# =======================================================================
# 测试用例4
# 解析 item
# =======================================================================
"""


def case_4():
    url = 'https://www.lagou.com/jobs/3451715.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'www.lagou.com',
        # 'Referer': 'http: //www.dytt8.net/html/gndy/dyzz/index.html',
    }

    proxies = {
        # 'http': random.choice(cls.Proxy_Pool),
        'http': 'web-proxy.oa.com:8080',
        # 'https': random.choice(cls.Proxy_Pool)
        'https': 'web-proxy.oa.com:8080',
    }

    response = requests.get(url, headers=headers, proxies=proxies, timeout=3)
    print(' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))
    selector = etree.HTML(response.text)

    keyword = selector.xpath("/html/body/div[2]/div/div[1]/div/span/text()")[0]
    print('keyword  ===  ' + keyword)


"""
# =======================================================================
# 测试用例5
# 测试定时任务 sched, 延迟 10 秒
# =======================================================================
"""


def case_5():
    print("===  case_5: " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "  ===")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(10, 1, __timed_task)
    scheduler.run()


def __timed_task():
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


"""
# =======================================================================
# 测试用例6
# 测试定时任务 Timer, 延迟 10 秒
# =======================================================================
"""


def case_6():
    Timer(10, __timed_task, ()).start()


"""
# =======================================================================
# 测试用例7
# 测试 APScheduler 定时框架, 延迟 10 秒
# =======================================================================
"""


def case_7():
    scheduler = BackgroundScheduler()  # BlockingScheduler  BackgroundScheduler
    scheduler.add_job(__timed_task, 'interval', seconds=2)
    scheduler.start()

    while True:
        print(time.time())
        time.sleep(5)


"""
# =======================================================================
# 测试用例8
# 从代理地址截取 ip 地址
# =======================================================================
"""


def case_8():
    proxy = 'http://58.60.255.82:8118'
    if 'http://' in proxy:
        proxy = proxy.replace('http://', '')
    else:
        proxy = proxy.replace('https://', '')

    proxy = proxy.split(':')[0]
    print(proxy)


"""
# =======================================================================
# 测试用例9
# 测试西刺爬虫
# =======================================================================
"""


def case_9():
    proxy_list = XiciSpider.get_proxies()
    print(proxy_list)


"""
# =======================================================================
# 测试用例 10
# 测试 ProxyDBManager 的 plus_proxy_faild_time(self, ip) 函数
# =======================================================================
"""


def case_10():

    dao = ProxyDBManager()
    dao.create_proxy_table()

    proxy = ProxyModel()

    ip = '125.115.141.6'
    port = 8118
    http_type = 'HTTPS'
    anonymity = '高匿'
    area = '浙江宁波'
    speed = '0.148秒'
    agent = 'agent'
    survival_time = '4小时'

    proxy.set_ip(ip)
    proxy.set_port(port)
    proxy.set_type(http_type)
    proxy.set_anonymity(anonymity)
    # 处理空地区
    if area is None:
        proxy.set_area('')
    else:
        proxy.set_area(area)
    proxy.set_speed(speed)
    proxy.set_agent(agent)
    proxy.set_survival_time(survival_time)

    dao.insert_proxy_table(proxy)

    proxy_address = dao.select_random_proxy()
    print(proxy_address)

    if 'http://' in proxy_address:
        proxy_address = proxy_address.replace('http://', '')
    else:
        proxy_address = proxy_address.replace('https://', '')

    old_ip = proxy_address.split(':')[0]
    print('old IP : ', old_ip)
    dao.plus_proxy_faild_time(old_ip)


'''
case_1()
case_2()
case_3()
case_4()
case_5()
case_6()
case_7()
case_8()
case_9()
'''
case_10()
