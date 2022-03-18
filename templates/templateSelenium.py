#!/usr/bin/python3
# -*- coding: utf-8 -*-



from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.remote_connection import RemoteConnection

###These 4 code lines is the most important and necessary code lines in yur code to connect to the browser side
PORT = 1222
#options = webdriver.ChromeOptions()
#options.add_argument(f'--remote-debugging-port={PORT}')
#options.add_argument('--headless')

#driver = webdriver.Chrome(options=options)

driver = WebDriver(f"http://127.0.0.1:{PORT}/wd/hub", "google", "ANY")

driver.get("http://www.instagram.com")

import time
time.sleep(10)

