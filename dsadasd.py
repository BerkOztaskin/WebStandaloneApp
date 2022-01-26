#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pychrome
from selenium import webdriver
from webdrivermanager import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=1234")
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

dev_tools = pychrome.Browser(url = 'http://localhost:1234')
tab = dev_tools.list()[0]
driver.get('https://fox.com')