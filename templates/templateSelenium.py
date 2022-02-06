#!/usr/bin/python3
# -*- coding: utf-8 -*-



from selenium import webdriver


###These 4 code lines is the most important and necessary code lines in yur code to connect to the browser side
PORT = 5555
options = webdriver.ChromeOptions()
options.add_argument(f'--remote-debugging-port={PORT}')
options.add_argument('--headless')
       


driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com")

import time
time.sleep(10)

