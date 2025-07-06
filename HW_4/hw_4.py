from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Настройка Firefox
options = Options()
options.add_argument('--headless')  # Убрать, если хотите видеть окно браузера
# Указать путь до geckodriver, если он не в PATH
service = Service(executable_path=ChromeDriverManager().install())  # Замените путь, если нужно

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
    title3 = driver.title
    time.sleep(2)
    print("Страница 3 TITLE:", title3)
    assert driver.title == title1, "Не удалось вернуться на первую страницу"
    print("Успешно вернулись назад.")
    # 4. Рефреш
    driver.refresh()
    time.sleep(2)
    current_url = driver.current_url
    print("Текущий URL после refresh:", current_url)

    #5. Вперёд
    driver.forward()
    title5 = driver.title
    new_url = driver.current_url
    print("Страница 5 TITLE:", title5)
    # 6. Проверка, что URL изменился
    print(new_url, current_url)
    assert new_url == current_url, "URL не изменился после перехода вперёд"
    print("URL успешно изменился — переход вперёд выполнен.")

finally:
    driver.quit()
