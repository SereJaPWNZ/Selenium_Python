from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://101hotels.com/")
time.sleep(2)

driver.get("https://101hotels.com/main/cities/moskva")
time.sleep(2)
driver.back
time.sleep(2)
driver.forward
time.sleep(2)
