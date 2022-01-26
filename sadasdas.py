from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


path = r"C:\Program Files (x86)\chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
#Change chrome driver path accordingly
chrome_driver = path
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print (driver.current_url)