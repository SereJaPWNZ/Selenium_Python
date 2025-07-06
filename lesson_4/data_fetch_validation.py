import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://101hotels.com/")

PAGE_URL = driver.current_url
PAGE_TITLE = driver.title
PAGE_SOURCE = driver.page_source

print("Page URL: ", PAGE_URL)
print("Page title: ", PAGE_TITLE)
#print("Page source: ", PAGE_SOURCE)

assert PAGE_URL == "https://101hotels.com/", "Ссылка не соответствует заданному значению."
assert PAGE_TITLE == "101HOTELS.com — отели живут здесь. Бронируйте гостиницы, базы отдыха, хостелы и другое жильё", "Заголовок не соответствует заданному значению."