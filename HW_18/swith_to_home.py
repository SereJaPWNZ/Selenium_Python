from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import platform


service = Service(executable_path=ChromeDriverManager().install())
options = Options()

# options.add_argument("--incognito")
options.add_argument("--window_size=1920,1080")

try:
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(2):
        driver.switch_to.new_window()
    open_tabs = driver.window_handles

    # Переключение на 1 вкладку с переходом по странице
    driver.switch_to.window(open_tabs[0])
    url_link_1 = "https://hyperskill.org/login"
    driver.get(url_link_1)
    # проверяем, что открылась нужная страница
    assert driver.current_url == url_link_1, "Перый урл не соответствует"
    # Выводим title страницы
    print(driver.title)

    # Переключение на 2 вкладку с переходом по странице
    driver.switch_to.window(open_tabs[1])
    url_link_2 = "https://www.avito.ru/"
    driver.get(url_link_2)
    # проверяем, что открылась нужная страница
    assert driver.current_url == url_link_2, "Второй урл не соответствует"
    # Выводим title страницы
    print(driver.title)


    # Переключение на 3 вкладку с переходом по странице
    driver.switch_to.window(open_tabs[2])
    url_link_3 = "https://4pda.to/"
    driver.get(url_link_3)
    time.sleep(10)
    # проверяем, что открылась нужная страница
    assert driver.current_url == url_link_3, "Третий урл не соответствует"
    # Выводим title страницы
    print(driver.title)
    time.sleep(500)


finally:
    driver.quit()
