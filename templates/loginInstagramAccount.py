#!/usr/bin/python3
# -*- coding: utf-8 -*-


from selenium import webdriver
import os.path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

PORT = 1222


class Browser:
    def __init__(self, link, username, password):
        self.link = link
        self.username = username
        self.password = password

        options = webdriver.ChromeOptions()

        options.add_argument(f'--remote-debugging-port={PORT}')
        # options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(self.link)
        self.waitLoad(4)
        import time
        time.sleep(10)
        self.login()
        time.sleep(20)
        self.driver.close()

    def login(self):
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.send_keys(self.username)
        password.send_keys(self.password)

        loginBtn = self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button")
        loginBtn.click()
        self.waitLoad(4)
        print('its finished')

    def waitUpload(self):
        wait = WebDriverWait(self.driver, 10)
        men_menu = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH,
                 "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/h2"
                 )))
        print(men_menu)
        self.driver.quit()

    def waitLoad(self, timeout):

        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")


Browser('https://www.instagram.com', 'berkinyenisi', 'berk998999')