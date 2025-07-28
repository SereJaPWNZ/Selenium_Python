from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--incognito")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#lOCATOR
DISPLAY_FOR_TIME = ("xpath", "//div[@id='deletesuccess']")
DELAYED_TEXT = ("xpath", "//div[@id='delayedText']")
TIMER_BTN = ("xpath", "//input[@id='timerButton']")
MY_BTN = ("xpath", "//button[@id='myBtn']")
TRY_IT= ("xpath","//button[text()='Try it']")

try:
    URL = "https://omayo.blogspot.com/"
    driver.get(URL)

    wait = WebDriverWait(driver, 30, poll_frequency=1)

    # 1. Ждём исчезновения надписи «success»
    wait.until(EC.invisibility_of_element_located(DISPLAY_FOR_TIME), message="Сообщение не пропало!")

    # 2. Ждём появления отложенного текста
    wait.until(EC.visibility_of_element_located(DELAYED_TEXT), message="Сообщение не появилось!")

    # 3. Ждём, пока Button3 станет активной, затем кликаем
    wait.until(EC.element_to_be_clickable(TIMER_BTN), message="Кнопка не стала активна").click()

    allert = driver.switch_to.alert
    allert.accept()

     # 4. Кликаем по My Button и ждём, пока она отключится
    wait.until(EC.element_to_be_clickable(MY_BTN), message="Кнопка не кликабельна, не прогрузилась или отсутствует").click()
    # Т.к. при клике на саму кнопку не срабатывает ее отключение, а кнопка рядом вызывает ее отключение, то заменим кнопку My Button, на Try it
    wait.until(EC.element_to_be_clickable(TRY_IT), message="Кнопка не кликабельна, не прогрузилась или отсутствует").click()
    time.sleep(3)
    # wait.until(EC.none_of(EC.element_to_be_clickable(MY_BTN), message="Кнопка кликабельна, ошибка"))
    # wait.until(EC.none_of(EC.visibility_of_element_located(MY_BTN), message="Кнопка кликабельна, ошибка"))
    wait.until(EC.element_attribute_to_include(MY_BTN, 'disabled'), 'Кнопка осталось активной')

finally:
    driver.quit()