# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : test_install_drivers.py
@Project            : S060_Selenium
@CreateTime         : 2023/5/9 16:31
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/5/9 16:31 
@Version            : 1.0
@Description        : None
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
import time


# @pytest.mark.skip(reason="Do not run in CI")
def test_driver_manager_chrome():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.baidu.com")
    time.sleep(10)
    driver.quit()


@pytest.mark.skip(reason="Do not run in CI")
def test_edge_session():
    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())

    driver = webdriver.Edge(service=service)

    driver.quit()


@pytest.mark.skip(reason="Do not run in CI")
def test_firefox_session():
    service = FirefoxService(executable_path=GeckoDriverManager().install())

    driver = webdriver.Firefox(service=service)

    driver.quit()


@pytest.mark.skip(reason="Do not run in CI")
def test_ie_session():
    service = IEService(executable_path=IEDriverManager().install())

    driver = webdriver.Ie(service=service)

    driver.quit()