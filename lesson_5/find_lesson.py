from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
options.add_argument("--incognito")
try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.freeconferencecall.com/ru/ru/login")
    time.sleep(2)
    driver.find_element("id", "loginformsubmit").click()
    time.sleep(2)

finally:
    driver.quit()