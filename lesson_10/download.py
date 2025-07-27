import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

download_dir = os.path.abspath(os.path.join(os.getcwd(), "downloads"))
os.makedirs(download_dir, exist_ok=True)

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("prefs", prefs)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    URL = "https://the-internet.herokuapp.com/download"
    driver.get(URL)
    files_xpath = "//div[@class='example']/a"
    files_texts = [el.text for el in driver.find_elements("xpath", files_xpath)]

    for text in files_texts:
        link = driver.find_element("xpath", f"//div[@class='example']/a[text()='{text}']")
        link.click()
        print(f"Начали скачивание файла {text}")
        time.sleep(10)  # здесь лучше проверять окончание загрузки файла
        break

finally:
    driver.quit()