import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep


service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe")

options = Options()
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
# options.add_argument("--headless")
options.add_argument("--incognito")

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://hyperskill.org/tracks")
    #2. Записать все xpath-локаторы, для всех элементов на странице https://hyperskill.org/tracks в формате кортежей
    HEADER = driver.find_elements("xpath", "//a[contains(@class, 'nav-link')]")
    BADGE = driver.find_elements("xpath", "//div/a[contains(@aria-current, 'page') and @click-event-target='category']")
    CARD = driver.find_elements("xpath", "//div[@data-component-name='TrackCard']")
    print(type(HEADER))
    print(type(BADGE))
    print(type(CARD))
finally:
    driver.quit()