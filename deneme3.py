#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


options = Options()
options.add_experimental_option("debuggerAddress","127.0.0.1:8888")
driver = webdriver.Chrome(executable_path="C:\\Users\GreyWolf\\UPWORK_PROJECTS\\WebBrowserBotStandaloneApp\\chromedriver.exe", chrome_options=options)

driver.get("")


time.sleep(100)