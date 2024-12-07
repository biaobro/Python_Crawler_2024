# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : scraper.py
@Project            : S013_Selenium_Reddit
@CreateTime         : 2024/12/7 10:09
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/12/7 10:09 
@Version            : 1.0
@Description        : None
"""
import json
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import myinit_webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# enable the headless mode
options = Options()
# options.add_argument('--headless=new')

# initialize a web driver to control Chrome
driver_path = myinit_webdriver.driver_init()
driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)

# max the controlled browser window
driver.fullscreen_window()

# scraping logic
url = 'https://www.reddit.com/r/technology/top/?t=week'
driver.get(url)

time.sleep(5)

subreddit = {}

# 直接从页面上提取元素
name = driver.find_element(By.TAG_NAME, 'h1').text
print(name)

creation_date = driver.find_element(By.XPATH, '//*[@id="subreddit-right-rail__partial"]/aside/div/shreddit-subreddit-header/div[3]/faceplate-tooltip[1]/div').text
print(creation_date)

# 页面上有个特殊元素 #shadow-root (open)，需要先获取到 shadow
# 才能获取 shadow 下的 description, create_date, members
shadow_host = driver.find_element(By.TAG_NAME, 'shreddit-subreddit-header')
shadow = driver.execute_script('return arguments[0].shadowRoot', shadow_host)

description = shadow.find_element(By.ID, "description").text
print(description)

members = shadow.find_element(By.ID, "subscribers").text
print(members)

subreddit['name'] = name
subreddit['description'] = description
subreddit['creation_date'] = creation_date
subreddit['members'] = members

print(subreddit)
exit()

posts = []

post_html_elements = driver \
    .find_elements(By.CSS_SELECTOR, '[data-testid="post-container"]')

for post_html_element in post_html_elements:
    post = {}

    # scraping logic...
    upvotes = post_html_element \
        .find_element(By.CSS_SELECTOR, '[data-click-id="upvote"]') \
        .find_element(By.XPATH, "following-sibling::*[1]") \
        .get_attribute('innerText')

    author = post_html_element \
        .find_element(By.CSS_SELECTOR, '[data-testid="post_author_link"]') \
        .text

    title = post_html_element \
        .find_element(By.TAG_NAME, 'h3') \
        .text

    try:
        outbound_link = post_html_element \
            .find_element(By.CSS_SELECTOR, '[data-testid="outbound-link"]') \
            .get_attribute('href')
    except NoSuchElementException:
        outbound_link = None

    comments = post_html_element \
        .find_element(By.CSS_SELECTOR, '[data-click-id="comments"]') \
        .get_attribute('innerText') \
        .replace(' Comments', '')

    # 使用检索到的数据填充字典
    post['upvotes'] = upvotes
    post['title'] = title
    post['outbound_link'] = outbound_link
    post['comments'] = comments

    # to avoid adding ad posts
    # to the list of scraped posts
    if title:
        posts.append(post)

subreddit['posts'] = posts

print(subreddit)

# close the browser and free up the Selenium resources
driver.quit()

# export the scraped data to a JSON file
with open('subreddit.json', 'w', encoding='utf-8') as file:
    json.dump(subreddit, file, indent=4, ensure_ascii=False)
