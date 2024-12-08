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

# 获取文章
posts = []

# 使用 class name 来定位元素
post_html_elements = driver.find_elements(By.CSS_SELECTOR, '.w-full.m-0')

for post_html_element in post_html_elements:
    post = {}

    try:
        # 通过标签名称来定位元素
        shreddit_post = post_html_element.find_element(By.TAG_NAME, 'shreddit-post')

        # scraping logic...
        # 获取标签的属性值
        comment_count = shreddit_post.get_attribute('comment-count')
        author = shreddit_post.get_attribute('author')
        title = shreddit_post.get_attribute('post-title')
        score = shreddit_post.get_attribute('score')
        create_timestamp = shreddit_post.get_attribute('created-timestamp')
        content_href = shreddit_post.get_attribute('content-href')

        # //shreddit-post/div/div[2]/div[3]/shreddit-post-flair/faceplate-tracker/a/span/div
        plate = shreddit_post.find_element(By.XPATH, 'div/div[2]/div[3]/shreddit-post-flair/faceplate-tracker/a/span/div').text
    except NoSuchElementException:
        continue

    # 使用检索到的数据填充字典
    post['comment_count'] = comment_count
    post['author'] = author
    post['title'] = title
    post['score'] = score
    post['create_timestamp'] = create_timestamp
    post['plate'] = plate

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
