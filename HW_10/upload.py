import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time


# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe")
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")

CHOOSE_FILE_UPLOAD_XPATH = "//input[@id='uploadFile']"

# Абсолютный путь к файлу:
download_dir = os.path.join(os.getcwd(), "HW_10","downloads")
print(download_dir)
file_name = "photo.png"
file_path = os.path.join(download_dir, file_name)
print("Файл для загрузки:", file_path)
assert os.path.exists(file_path), f"Файл не найден: {file_path}"

UPLOAD_FILE_XPATH = f"//div[@id='uploaded-files' and contains(text(), '{file_name}')]"

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://demoqa.com/upload-download")
    time.sleep(10)
    search_CHOOSE_FILE_XPATH = driver.find_element("xpath", CHOOSE_FILE_UPLOAD_XPATH)
    search_CHOOSE_FILE_XPATH.send_keys(file_path)
    time.sleep(3)

    uploaded = driver.find_element("xpath", "//p[@id='uploadedFilePath']").text.strip()
    assert uploaded == f"C:\\fakepath\{file_name}", "Ошибка в название файла"

finally:
    driver.quit()