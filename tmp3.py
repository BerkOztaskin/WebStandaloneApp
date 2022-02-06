#!/usr/bin/python3
# -*- coding: utf-8 -*-



from selenium import webdriver

PORT = 5555


class Browser:
    def __init__(self, link):
        self.link = link


        options = webdriver.ChromeOptions()

        options.add_argument(f'--remote-debugging-port={PORT}')
        options.add_argument('--headless')
       


        self.driver = webdriver.Chrome(options=options)

        self.driver.get(self.link)

        import time
        time.sleep(10)



Browser('https://www.instagram.com')