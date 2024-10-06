# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 073_twitter_article.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/10/6 15:11
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/10/6 15:11 
@Version            : 1.0
@Description        : None
"""
import time

from selenium import webdriver
import myinit_webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

######################################
# 需要登录态才能访问
######################################
website = 'https://x.com/search?q=python&src=typed_query'
# website = 'https://s.weibo.com/weibo?q=python'

# 得到 driver 所在路径
driver_path = myinit_webdriver.driver_init()

# 初始化 driver
driver = webdriver.Chrome(service=ChromeService(driver_path))
driver.get(website)
driver.maximize_window()
time.sleep(2)


# 列表，集合，元组
posterAccounts = []
contents = []
tweetIds = set()

scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))

    for tweet in tweets[-15:]:
        try:
            posterAccount = tweet.find_element(By.XPATH, ".//span[contains(text(),'@')]").text
            content = tweet.find_element(By.XPATH, ".//div[@lang]").text
            # split() 无指定入参时按照空格、回车、换行进行分割
            content = ' '.join(content.split())
        except:
            posterAccount = 'account'
            content = 'content'

        tweetId = ''.join([posterAccount, content])
        if tweetId not in tweetIds:
            tweetIds.add(tweetId)
            posterAccounts.append(posterAccount)
            contents.append(content)

    # 慎用！！！ 请找1个页面内容不多的场景测试
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            scrolling = False
            break
        else:
            lastHeight = newHeight
            break

driver.quit()

# save to file
df = pd.DataFrame({'posterAccount': posterAccounts, 'content': contents})
df.to_csv('tweets.csv', index=False)
print(df)
