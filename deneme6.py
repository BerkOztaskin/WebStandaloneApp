#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


CHROME_PATH = 'C:\\Users\\GreyWolf\\UPWORK_PROJECTS\\WebBrowserBotStandaloneApp\\chromedriver.exe'
options = Options()
options.add_argument('--remote-debugging-port=3333')
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://instagram.com")


time.sleep(100)