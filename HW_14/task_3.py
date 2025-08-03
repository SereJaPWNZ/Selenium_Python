from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import pickle
import time

# --- Настройки Selenium ---
service = Service(executable_path=ChromeDriverManager().install())
options_chrome = Options()
options_chrome.add_argument("--incognito")
# options_chrome.add_argument("--headless")

# --- Локаторы ---
email_xpath = ("xpath", "//div[@class='main empty-main']//input[@type='email']")
password_xpath = ("xpath", "//div[@class='main empty-main']//input[@type='password']")
submit_xpath = ("xpath", "//div[@class='main empty-main']//button[@type='submit']")
bonus_xpath = ("xpath", "//span[@class='account-bonus-val']")
captcha_xpath = ("xpath", "//div[@id='rc-imageselect']")

# --- Путь к файлам ---
cookie_path = os.path.join("HW_14", "cookies", "cookies.pkl")
screenshot_path = os.path.join("HW_14", "screenshot", "tools.png")

# --- Убедимся, что папки есть ---
os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)


def login(driver, wait):
    """Ввод логина и пароля, клик по кнопке входа"""
    driver.get("https://secure.101hotels.com/account")
    wait.until(EC.element_to_be_clickable(email_xpath)).send_keys("EMAIL")
    wait.until(EC.element_to_be_clickable(password_xpath)).send_keys("PASSWORD")
    wait.until(EC.element_to_be_clickable(submit_xpath)).click()


def handle_captcha(wait):
    """Ожидание капчи и пауза для ручного решения"""
    try:
        wait.until(EC.presence_of_element_located(captcha_xpath))
        print("Капча обнаружена — требуется ручной ввод.")
        input("Реши капчу и нажми Enter для продолжения...")
    except TimeoutException:
        print("Капча не появилась — продолжаем без неё.")


def save_cookies(driver):
    with open(cookie_path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookies(driver):
    with open(cookie_path, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


# --- Основной блок ---
try:
    driver = webdriver.Chrome(service=service, options=options_chrome)
    wait = WebDriverWait(driver, 30, 0.5)

    # Вход с возможной капчей
    login(driver, wait)
    handle_captcha(wait)

    # Проверка успешного входа с ограничением попыток
    attempts = 0
    while driver.current_url == "https://secure.101hotels.com/account/login" and attempts < 3:
        print("Неудачный вход. Повторная попытка...")
        login(driver, wait)
        handle_captcha(wait)
        attempts += 1

    if driver.current_url == "https://secure.101hotels.com/account/login":
        print("Слишком много неудачных попыток входа.")
    else:
        # Успешный вход
        wait.until(EC.element_to_be_clickable(bonus_xpath))
        save_cookies(driver)
        driver.delete_all_cookies()

        # Перезаход с cookies
        driver.get("https://secure.101hotels.com/account")
        load_cookies(driver)
        driver.refresh()

        wait.until(EC.element_to_be_clickable(bonus_xpath))
        driver.save_screenshot(screenshot_path)
        print("Готово: бонус доступен, скриншот сделан.")

finally:
    driver.quit()
