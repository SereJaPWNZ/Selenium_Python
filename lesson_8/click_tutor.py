from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
# options.add_argument("--incognito")

LOG_IN = ("xpath", "//a[@href='/login']")
EMAIL_INPUT = ("xpath", "//input[@id='login_email']")
PASSWORD_INPUT = ("xpath", "//input[@id='password']")
try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.freeconferencecall.com")
    sleep(10)
    driver.find_element(*LOG_IN).click()
    sleep(1)
    driver.find_element(*EMAIL_INPUT).send_keys("test@test.test")
    driver.find_element(*PASSWORD_INPUT).send_keys("test1test")
    sleep(1)
    driver.find_element(*EMAIL_INPUT).clear()
    sleep(10)

finally:
    driver.quit()