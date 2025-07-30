"""
Исправленный Selenium-скрипт для автоматизации тестирования модальных окон
Применены все лучшие практики: POM, логирование, обработка ошибок, конфигурация
"""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    WebDriverException, 
    NoAlertPresentException
)


@dataclass
class Config:
    """Конфигурация для Selenium WebDriver"""
    webdriver_path: str = r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe"
    browser_path: str = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
    base_url: str = "https://demoqa.com/alerts"
    explicit_wait: int = 10
    screenshot_dir: str = "lesson_13/screenshots"
    window_size: Tuple[int, int] = (1920, 1080)
    headless: bool = True


class Logger:
    """Централизованное логирование"""
    
    @staticmethod
    def setup_logger(name: str = "selenium_alerts") -> logging.Logger:
        """Настраивает и возвращает logger"""
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger
            
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger


class WebDriverManager:
    """Менеджер для управления WebDriver"""
    
    def __init__(self, config: Config):
        self.config = config
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = Logger.setup_logger("WebDriverManager")
    
    def setup_driver(self) -> WebDriver:
        """Настраивает и возвращает WebDriver"""
        try:
            service = Service(executable_path=self.config.webdriver_path)
            options = Options()
            options.binary_location = self.config.browser_path
            options.add_argument("--incognito")
            options.add_argument(f"--window-size={self.config.window_size[0]},{self.config.window_size[1]}")
            
            if self.config.headless:
                options.add_argument("--headless")
            
            # Дополнительные настройки для стабильности
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, self.config.explicit_wait, poll_frequency=1)
            
            self.logger.info("WebDriver успешно инициализирован")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Ошибка при инициализации WebDriver: {e}")
            raise WebDriverException(f"Не удалось инициализировать WebDriver: {e}")
    
    @contextmanager
    def get_driver(self):
        """Контекстный менеджер для WebDriver"""
        driver = None
        try:
            driver = self.setup_driver()
            yield driver, self.wait
        except Exception as e:
            self.logger.error(f"Ошибка в контекстном менеджере: {e}")
            raise
        finally:
            if driver:
                driver.quit()
                self.logger.info("WebDriver закрыт")


class AlertsPage:
    """Page Object для страницы с alert'ами - исправленная версия исходного кода"""
    
    # Локаторы (исправлены, используется By вместо строк)
    ALERT_1_BUTTON = (By.XPATH, "//button[@id='alertButton']")
    ALERT_2_BUTTON = (By.XPATH, "//button[@id='timerAlertButton']")  
    ALERT_3_BUTTON = (By.XPATH, "//button[@id='confirmButton']")
    ALERT_4_BUTTON = (By.XPATH, "//button[@id='promtButton']")
    CONFIRM_RESULT = (By.XPATH, "//span[@id='confirmResult']")
    PROMPT_RESULT = (By.XPATH, "//span[@id='promptResult']")
    
    def __init__(self, driver: WebDriver, wait: WebDriverWait, config: Config):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.logger = Logger.setup_logger("AlertsPage")
        self.alert = None  # Для хранения текущего alert
    
    def click_button(self, locator_button: Tuple[By, str]) -> None:
        """
        Исправленная функция: click_button с proper error handling
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator_button))
            element.click()
            self.logger.info(f"Клик по кнопке {locator_button[1]} выполнен")
        except TimeoutException:
            self.logger.error(f"Кнопка {locator_button[1]} не найдена или не кликабельна")
            self.save_screenshot("click_button_error")
            raise
        except Exception as e:
            self.logger.error(f"Ошибка при клике: {e}")
            raise

    def focus_to_alert(self) -> None:
        """
        Исправленная функция: focus_to_alert с proper alert handling
        """
        try:
            self.alert = self.wait.until(EC.alert_is_present())
            self.driver.switch_to.alert
            self.logger.info("Фокус переведен на alert")
        except TimeoutException:
            self.logger.error("Alert не появился в ожидаемое время")
            raise NoAlertPresentException("Alert не найден")
        except Exception as e:
            self.logger.error(f"Ошибка при переводе фокуса на alert: {e}")
            raise

    def assertAlertText(self, expectedAlertText: str = None, alertNumber: int = 1) -> None:
        """
        Исправленная функция: assertAlertText с proper validation
        """
        try:
            if self.alert is None:
                raise ValueError("Alert не инициализирован. Вызовите focus_to_alert() сначала")
            
            actual_text = self.alert.text
            if actual_text != expectedAlertText:
                error_msg = f"Alert {alertNumber}: ожидался '{expectedAlertText}', получен '{actual_text}'"
                self.logger.error(error_msg)
                raise AssertionError(error_msg)
            
            self.logger.info(f"Текст alert {alertNumber} корректен: '{actual_text}'")
            
        except Exception as e:
            self.logger.error(f"Ошибка при проверке текста alert: {e}")
            raise

    def save_screenshot(self, number_screenshot: str = "1") -> str:
        """
        Исправленная функция: save_screenshot с path handling
        """
        try:
            # Создаем директорию если её нет
            Path(self.config.screenshot_dir).mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alert_{number_screenshot}_{timestamp}.png"
            filepath = os.path.join(self.config.screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Скриншот сохранен: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Ошибка при создании скриншота: {e}")
            raise

    def accept_alert(self) -> None:
        """
        Исправленная функция: accept_alert с error handling
        """
        try:
            if self.alert is None:
                raise ValueError("Alert не инициализирован")
            
            self.alert.accept()
            self.alert = None  # Очищаем после закрытия
            self.logger.info("Alert принят")
            
        except Exception as e:
            self.logger.error(f"Ошибка при принятии alert: {e}")
            raise

    def dismiss_alert(self) -> None:
        """
        Исправленная функция: dismiss_alert с error handling
        """
        try:
            if self.alert is None:
                raise ValueError("Alert не инициализирован")
            
            self.alert.dismiss()
            self.alert = None  # Очищаем после закрытия
            self.logger.info("Alert отклонен")
            
        except Exception as e:
            self.logger.error(f"Ошибка при отклонении alert: {e}")
            raise

    def expectedText(self, locator_without_xpath: str, text: str) -> None:
        """
        Исправленная функция: expectedText с proper locator handling
        """
        try:
            locator = (By.XPATH, locator_without_xpath)
            
            if locator_without_xpath == "//span[@id='promptResult']":
                expected_text = f"You entered {text}"
            else:
                expected_text = text
            
            self.wait.until(EC.text_to_be_present_in_element(locator, expected_text))
            self.logger.info(f"Ожидаемый текст '{expected_text}' найден в элементе")
            
        except TimeoutException:
            self.logger.error(f"Текст '{expected_text}' не найден в элементе {locator_without_xpath}")
            self.save_screenshot("text_verification_error")
            raise
        except Exception as e:
            self.logger.error(f"Ошибка при проверке текста: {e}")
            raise

    def send_keys_alert(self, text: str = "text") -> None:
        """
        Исправленная функция: send_keys_alert с validation
        """
        try:
            if self.alert is None:
                raise ValueError("Alert не инициализирован")
            
            self.alert.send_keys(text)
            self.logger.info(f"В alert введен текст: '{text}'")
            
        except Exception as e:
            self.logger.error(f"Ошибка при вводе текста в alert: {e}")
            raise


def main():
    """
    Исправленная главная функция с применением всех улучшений
    """
    config = Config()
    logger = Logger.setup_logger("main")
    
    logger.info("=== ЗАПУСК ТЕСТОВ ALERTS ===")
    
    driver_manager = WebDriverManager(config)
    
    try:
        with driver_manager.get_driver() as (driver, wait):
            # Инициализируем Page Object
            alerts_page = AlertsPage(driver, wait, config)
            
            # Загружаем страницу
            driver.get(config.base_url)
            logger.info(f"Страница {config.base_url} загружена")
            
            # Тест 1: Простой alert
            logger.info("--- Тест 1: Простой alert ---")
            alerts_page.click_button(alerts_page.ALERT_1_BUTTON)
            alerts_page.focus_to_alert()
            alerts_page.assertAlertText("You clicked a button", 1)
            alerts_page.accept_alert()
            
            # Тест 2: Alert с таймером
            logger.info("--- Тест 2: Alert с таймером ---")
            alerts_page.click_button(alerts_page.ALERT_2_BUTTON)
            alerts_page.focus_to_alert()
            alerts_page.assertAlertText("This alert appeared after 5 seconds", 2)
            alerts_page.accept_alert()
            
            # Тест 3: Confirm alert - принятие
            logger.info("--- Тест 3: Confirm alert (принятие) ---")
            alerts_page.click_button(alerts_page.ALERT_3_BUTTON)
            alerts_page.focus_to_alert()
            alerts_page.assertAlertText("Do you confirm action?", 3)
            alerts_page.accept_alert()
            alerts_page.expectedText("//span[@id='confirmResult']", "You selected Ok")
            
            # Тест 4: Confirm alert - отклонение
            logger.info("--- Тест 4: Confirm alert (отклонение) ---")
            alerts_page.click_button(alerts_page.ALERT_3_BUTTON)
            alerts_page.focus_to_alert()
            alerts_page.assertAlertText("Do you confirm action?", 3)
            alerts_page.dismiss_alert()
            alerts_page.expectedText("//span[@id='confirmResult']", "You selected Cancel")
            
            # Тест 5: Prompt alert
            logger.info("--- Тест 5: Prompt alert ---")
            test_text = "test_text"
            alerts_page.click_button(alerts_page.ALERT_4_BUTTON)
            alerts_page.focus_to_alert()
            alerts_page.assertAlertText("Please enter your name", 4)
            alerts_page.send_keys_alert(test_text)
            alerts_page.accept_alert()
            alerts_page.expectedText("//span[@id='promptResult']", test_text)
            alerts_page.save_screenshot("final")
            
            logger.info("=== ВСЕ ТЕСТЫ ВЫПОЛНЕНЫ УСПЕШНО ===")
            
    except Exception as e:
        logger.error(f"Критическая ошибка при выполнении тестов: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
