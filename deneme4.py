#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:1111")
driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=options)

driver.get("http://instagram.com")


time.sleep(100)