from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Настройка Firefox
options = Options()
options.add_argument('--headless')  # Убрать, если хотите видеть окно браузера

# Указать путь до geckodriver, если он не в PATH
service = Service(executable_path=GeckoDriverManager().install())  # Замените путь, если нужно

# Инициализация драйвера
driver = webdriver.Firefox(service=service, options=options)

try:
    # 1. Открыть первую страницу
    driver.get("https://101hotels.com")
    time.sleep(2)  # Подождем для стабильности
    title1 = driver.title
    print("Страница 1 TITLE:", title1)

    # 2. Открыть вторую страницу
    driver.get("https://101hotels.com/main/cities/moskva")
    time.sleep(2)
    title2 = driver.title
    print("Страница 2 TITLE:", title2)

    # 3. Вернуться назад
    driver.back()
    driver.back()
    time.sleep(2)
    assert driver.title == title1, "Не удалось вернуться на первую страницу"
    print("Успешно вернулись назад.")
    
    # 4. Рефреш
    driver.refresh()
    time.sleep(2)
    current_url = driver.current_url
    print("Текущий URL после refresh:", current_url)

    # 5. Вперёд
    driver.forward()
    time.sleep(2)
    new_url = driver.current_url
    print("Текущий URL после перехода вперёд:", new_url)

    # 6. Проверка, что URL изменился
    assert new_url != current_url, "URL не изменился после перехода вперёд"
    print("URL успешно изменился — переход вперёд выполнен.")

finally:
    driver.quit()
