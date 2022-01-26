from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


CHROME_PATH = 'C:\\Users\\GreyWolf\\UPWORK_PROJECTS\\WebBrowserBotStandaloneApp\\chromedriver.exe'
options = Options()
#options.add_experimental_option("debuggerAddress", "localhost:2222")
options.add_argument('--remote-debugging-port=3333')
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://facebook.com")


time.sleep(100)