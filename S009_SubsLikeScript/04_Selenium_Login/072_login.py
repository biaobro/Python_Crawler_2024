# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 072_login.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/22 12:51
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/22 12:51 
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

website = 'https://www.zhihu.com/signin?next=%2F'

# 得到 driver 所在路径
driver_path = myinit_webdriver.driver_init()

# 初始化 driver
driver = webdriver.Chrome(service=ChromeService(driver_path))
driver.get(website)
driver.maximize_window()

time.sleep(2)

# 找到登录tabs
tabs = driver.find_elements(By.CLASS_NAME, 'SignFlow-tab')

# 切换到密码登录
tabs[1].click()

# 找到用户名和密码输入框
username = driver.find_element(By.XPATH, "//input[@name='username']")
password = driver.find_element(By.XPATH, "//input[@name='password']")

# 发送用户名和密码
username.send_keys('biaobro@sina.com')
password.send_keys('Mzxws@2020')

# 点击登录按钮
loginButton = driver.find_element(By.XPATH, "//button[@type='submit']")
loginButton.click()

time.sleep(3)

# 到这步就可以了，下一步是滑块
driver.quit()