# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : test_first_script.py
@Project            : S060_Selenium
@CreateTime         : 2023/5/9 16:38
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/5/9 16:38 
@Version            : 1.0
@Description        : None
"""
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_eight_components():
    driver = webdriver.Chrome()

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    driver.quit()
