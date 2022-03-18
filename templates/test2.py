#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import random
import os.path
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


###These 4 code lines is the most important and necessary code lines in yur code to connect to the browser side
PORT = 1222
options = webdriver.ChromeOptions()

#options.add_argument(f'--remote-debugging-port={PORT}')
options.add_argument('--auto-open-devtools-for-tabs')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
###  

goog = "https:/www.google.com/"
tm_rnd = [3,5]

driver.get(goog)

def slp():
    tm_rnd = [3,5]
    return random.randint(tm_rnd[0], tm_rnd[1])

def check_exists(text):
    xpath = '//*[contains(text(), \'' + text + '\')]'
    try:
        el = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return el

words_to_find = ['submit']

while True:
    slp()
    print(words_to_find)
    for w in words_to_find:
        el = check_exists(w)
        if el != False:
            print(f"Found {w}")
            el.click()

