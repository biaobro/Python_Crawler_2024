# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 060_clickButton.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/18 22:47
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/18 22:47
@Version            : 1.0
@Description        : None
"""
import time

from selenium.webdriver.common.by import By

import myinit_webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'
driver_path = myinit_webdriver.driver_init()
driver = webdriver.Chrome(service=ChromeService(driver_path))
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()
time.sleep(10)

dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Spain')
time.sleep(5)

matches = driver.find_elements(By.TAG_NAME, 'tr')

# range() 如果不指定，就是从0开始
date, home_team, score, away_team = [[] for x in range(4)]
for match in matches:
    # //tr/td[]
    try:
        # 根据页面结构，只记录包含4列的行中的值
        tds = len(match.find_elements(By.XPATH, './td'))
        if tds == 4:
            date.append(match.find_element(By.XPATH, './td[1]').text)
            home_team.append(match.find_element(By.XPATH, './td[2]').text)
            score.append(match.find_element(By.XPATH, './td[3]').text)
            away_team.append(match.find_element(By.XPATH, './td[4]').text)
            # print(match.text)
            # print(date, home_team, score, away_team)
    except:
        pass
driver.quit()

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)

