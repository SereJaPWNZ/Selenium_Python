import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time


# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe", log_path=os.devnull)
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
# Текущая папка скрипта/запуска
current_dir = os.getcwd()
download_dir = os.path.join(current_dir, "lesson__10", "downloads")

prefs = {
    "download.default_directory": download_dir,  # куда сохранять файлы
    "download.prompt_for_download": False,       # не спрашивать куда сохранять, сразу скачивать
    "download.directory_upgrade": True,          # обновление директории загрузки
    "safebrowsing.enabled": True                  # разрешить безопасные загрузки
}
options.add_experimental_option("prefs", prefs)


try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://the-internet.herokuapp.com/download")
    files_xpath = "//div[@class='example']/a"
    files_text = [el.text for el in driver.find_elements("xpath", files_xpath)]

    for text in files_text:
        print(f"Производим поиск файла {text}")
        link = driver.find_element("xpath", f"//div[@class='example']/a[text()='{text}']")
        print(link)
        link.click()
        time.sleep(10)
        break

finally:
    driver.quit()