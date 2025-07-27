from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--start-maximized")

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--disable-cache")

# －Методы из видео:
# ➖ Добавление новой опции - add_argument("--имя_опции")
# ➖ Установка размера окна - driver.set_window_size(1920, 1080)
# ➖ Развернуть окно браузера на весь экран - driver.maximize_window()

# Хардкдинг стратегии загрузки:
# ➖ chrome_options.page_load_strategy = "normal" - дожидается загрузки всех ресурсов
# ➖ chrome_options.page_load_strategy = "eager" - дожидается загрузки DOM



try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    URl = "https://whatismyipaddress.com/"
    driver.get(URl)
    print(driver.title)

finally:
    driver.quit()