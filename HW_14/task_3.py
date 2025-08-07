import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pickle

# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")

# locator
account_button_xpath = ("xpath", "//div[@class='account dropdown pull-right']")
email_field_xpath = ("xpath", "//input[@id='client-email']")
password_field_xpath = ("xpath", "//input[@id='client-password']")
login_button_xpath = ("xpath", "//button[contains(@class, 'login-submit')]")
eye_xpath = ("xpath", "//form[@id='login-form']//span[@class='fa fa-eye']")
bonus_xpath = ("xpath", "//div[@class='account-bonus-wrap']")

try:
    driver = webdriver.Chrome(service=service, options=options)
    
    wait = WebDriverWait(driver, 30, 1)
    driver.get("https://101hotels.com/")

    account_button = wait.until(EC.element_to_be_clickable(account_button_xpath))
    account_button.click()

    wait.until(EC.element_to_be_clickable(email_field_xpath)).send_keys("m101serg@gmail.com")
    
    wait.until(EC.element_to_be_clickable(password_field_xpath)).send_keys("test1test")

    wait.until(EC.element_to_be_clickable(eye_xpath)).click()


    

    wait.until(EC.element_to_be_clickable(login_button_xpath)).click()
    wait.until(EC.element_to_be_clickable(bonus_xpath))
    


    driver.save_screenshot("HW_14/screenshot/test_screenshot.png")


finally:
    driver.quit()