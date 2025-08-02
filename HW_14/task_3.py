import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pickle

# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe")
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")

# locator
buy_button = ("xpath", "//button[text()='Купить']")
card_button = ("xpath", "//div[@class='cart-button']")


try:
    driver = webdriver.Chrome(service=service, options=options)
    
    wait = WebDriverWait(driver, 30, 1)
    driver.get("https://www.dns-shop.ru/product/710936a51968d0a4/121-planset-xiaomi-redmi-pad-pro-wi-fi-256-gb-seryj/")

    wait.until(EC.element_to_be_clickable(buy_button)).click()
    
    pickle.dump(driver.get_cookies(), open(os.getcwd() + "HW_14/cookies/cookies.pkl", "wb"))
    
    driver.delete_all_cookies()

    cookies = pickle.load(open(os.getcwd()+"HW_14/cookies/cookies.pkl", "rb"))
    driver.refresh()

    wait.until(EC.element_to_be_clickable(buy_button))
    wait.until(EC.element_to_be_clickable(card_button)).click()
    wait.until(EC.element_to_be_clickable("xpath", "//div[@class='buy-button-wrapper']"))
    driver.save_screenshot("HW_14/screenshot/test_screenshot.png")

finally:
    driver.quit()