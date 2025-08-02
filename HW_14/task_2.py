import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe")
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")

# locator
email_field = ("xpath", "//div[@class='main empty-main']//input[@placeholder='Электронная почта*']")
password_field = ("xpath", "//div[@class='main empty-main']//input[@type='password']")
sign_in = ("xpath", "//div[@class='main empty-main']//button[@type='submit']")
test = ("xpath", "//div[@class='account-status-info--title']")


try:
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 30, 1)
    driver.get("https://secure.101hotels.com/account")

    wait.until(EC.element_to_be_clickable(email_field))
    driver.delete_cookie("h101dc")

    for cookie in driver.get_cookies():
        if cookie["name"] == "h101dc":
            print("удаление куки не сработало")
            break

finally:
    driver.quit()