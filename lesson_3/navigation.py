from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\chrome_driver_win64\chromedriver.exe")
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://101hotels.com/")
time.sleep(2)

driver.get("https://101hotels.com/main/cities/moskva")
time.sleep(2)
driver.back
time.sleep(2)
driver.forward
time.sleep(2)
