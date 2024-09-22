# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : 062_buildBot.py
@Project            : S009_SubsLikeScript
@CreateTime         : 2024/9/21 11:57
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/9/21 11:57 
@Version            : 1.0
@Description        : None
"""
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import myinit_webdriver

website = 'https://www.audible.com/search'

# 得到 driver 所在路径
driver_path = myinit_webdriver.driver_init()

# 初始化 driver， 使用无头模式
options = Options()
# options.add_argument("headless")
# options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)

# 请求网址
driver.get(website)
driver.maximize_window()

# 翻页 pagination
pagination = driver.find_element(By.CLASS_NAME, "pagingElements")
lastPage = int(pagination.find_elements(By.XPATH, './/li')[-2].text)
currentPage = 1

# 拆解具体内容
imgUrls, titles, authors, lengths, releaseDates, languages, ratings, prices, sampleVideos = [[] for x in range(9)]

while currentPage <= lastPage:
    # Implicit wait
    # time.sleep(10)

    # 得到 product list
    # products = driver.find_elements(By.XPATH, '//li[contains(@class, "productListItem")]')

    # Explict wait
    # 最多等待5s，如果在5s 内 until 指定的条件得到满足，则不再等待
    # 注意 presence_of_all_elements_located 得到的是 elements
    # presence_of_all_element_located 得到的是 element
    products = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "productListItem")]')))
    print(len(products))

    for product in products:
        imgUrl = product.find_element(By.XPATH, './/img[contains(@class,"bc-pub-block")]').get_attribute('src')
        title = product.find_element(By.XPATH, './/h3[contains(@class,"bc-heading")]').text
        author = product.find_element(By.XPATH, './/li[contains(@class,"authorLabel")]//a').text
        length = product.find_element(By.XPATH, './/li[contains(@class,"runtimeLabel")]').text.split(':')[1].strip()
        releaseDate = product.find_element(By.XPATH, './/li[contains(@class,"releaseDateLabel")]').text.split(':')[
            1].strip()
        language = product.find_element(By.XPATH, './/li[contains(@class,"languageLabel")]').text.split(':')[1].strip()
        rating = product.find_element(By.XPATH,
                                      './/li[contains(@class,"ratingsLabel")]//span[contains(@class,'
                                      '"bc-color-secondary")]').text
        price = product.find_element(By.XPATH, './/p[contains(@class,"buybox-regular-price")]').text.split(':')[1].strip()

        # 不是所有 product 都提供 SampleVideo
        try:
            sampleVideo = product.find_element(By.XPATH, './/button').get_attribute('data-mp3')
            print(sampleVideo)
        except:
            sampleVideo = ''

        imgUrls.append(imgUrl)
        titles.append(title)
        authors.append(author)
        lengths.append(length)
        releaseDates.append(releaseDate)
        languages.append(language)
        ratings.append(rating)
        prices.append(price)
        sampleVideos.append(sampleVideo)

        # break
    currentPage += 1
    try:
        nextPage = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        nextPage.click()
    except:
        pass

    if currentPage == 5:
        break

driver.quit()

# 初始化 DataFrame
df = pd.DataFrame(
    {'imgUrl': imgUrls, 'title': titles, 'author': authors, 'length': lengths, 'releaseDate': releaseDates,
     'language': languages, 'rating': ratings, 'price': prices, 'sampleVideo': sampleVideos})

# 将DataFrame 保存成 csv
df.to_csv('audiobooks.csv', index=False)
