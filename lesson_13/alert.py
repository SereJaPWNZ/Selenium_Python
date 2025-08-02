import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Указываем путь до yandexdriver.exe (скачали и распаковали заранее)
service = Service(executable_path=r"C:\Users\Sergey\Documents\MyProjectSelenium\Selenium_Python\webdriver\yandexdriver.exe")
options = Options()
# Путь до установленного браузера Яндекс. Обратите внимание, что папка может отличаться в зависимости от способа установки и версии.
options.binary_location = r"C:\Users\Sergey\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")

# Локаторы кнопок
ALERT_1_BUTTON = ("xpath", "//button[@id='alertButton']")
ALERT_2_BUTTON = ("xpath", "//button[@id='timerAlertButton']")
ALERT_3_BUTTON = ("xpath", "//button[@id='confirmButton']")
ALERT_4_BUTTON = ("xpath", "//button[@id='promtButton']")

# Функции
def click_button(locator_button: list) -> None:
    """
    Нажимает на кнопку, определенную локатором.
    
    Args:
        locator_button (list): Локатор кнопки в формате (тип, значение)
        
    Returns:
        None
        
    Описание:
        Функция ожидает, пока кнопка станет кликабельной, а затем выполняет клик по ней.
        Использует WebDriverWait для ожидания готовности элемента.
    """
    wait.until(EC.element_to_be_clickable(locator_button)).click()
    return None

def focus_to_alert() -> None:
    """
    Переводит фокус на появившееся модальное окно (alert).
    
    Returns:
        None
        
    Описание:
        Функция ожидает появления alert на странице и переключает на него фокус.
        Необходима для дальнейшей работы с модальным окном.
    """
    alert = wait.until(EC.alert_is_present())
    driver.switch_to.alert
    return None

def assertAlertText(expectedAlertText = None, alertNumber = 1) -> None:
    """
    Проверяет текст в модальном окне (alert).
    
    Args:
        expectedAlertText (str, optional): Ожидаемый текст в alert. По умолчанию None.
        alertNumber (int, optional): Номер alert для отображения в сообщении об ошибке. По умолчанию 1.
        
    Returns:
        None
        
    Raises:
        AssertionError: Если текст в alert не совпадает с ожидаемым
        
    Описание:
        Функция сравнивает фактический текст в alert с ожидаемым текстом.
        В случае несовпадения выбрасывает исключение с информативным сообщением.
    """
    assert alert.text == expectedAlertText, f"Что-то не так с/cо {alertNumber} алертом"
    return None

def save_screenshot(number_screenshot = "1") -> None:
    """
    Сохраняет скриншот текущего состояния браузера.
    
    Args:
        number_screenshot (str, optional): Номер скриншота для имени файла. По умолчанию "1".
        
    Returns:
        None
        
    Описание:
        Функция создает скриншот текущей страницы и сохраняет его в папку 
        lesson_13/screenshots/ с именем alert_[номер].png
    """
    driver.save_screenshot(f"lesson_13/screenshots/alert_{number_screenshot}.png")
    return None

def accept_alert() -> None:
    """
    Принимает (подтверждает) модальное окно alert.
    
    Returns:
        None
        
    Описание:
        Функция нажимает кнопку "OK" в модальном окне, что эквивалентно 
        подтверждению действия в alert.
    """
    alert.accept()
    return None

def dismiss_alert() -> None:
    """
    Отклоняет (отменяет) модальное окно alert.
    
    Returns:
        None
        
    Описание:
        Функция нажимает кнопку "Cancel" в модальном окне, что эквивалентно 
        отмене действия в alert.
    """
    alert.dismiss()
    return None

def expectedText(locator_without_xpath, text) -> None:
    """
    Ожидает появления определенного текста в элементе на странице.
    
    Args:
        locator_without_xpath (str): XPath локатор элемента без префикса "xpath"
        text (str): Ожидаемый текст в элементе
        
    Returns:
        None
        
    Описание:
        Функция ожидает появления указанного текста в элементе страницы.
        Для элемента с id 'promptResult' добавляет префикс "You entered ".
        Для всех остальных элементов использует текст как есть.
    """
    if locator_without_xpath == "//span[@id='promptResult']":
        wait.until(EC.text_to_be_present_in_element(("xpath", locator_without_xpath), f"You entered {text}"))
    else:
        wait.until(EC.text_to_be_present_in_element(("xpath", locator_without_xpath), f"{text}"))
    return None

def send_keys_alert(text = "text") -> None:
    """
    Вводит текст в поле ввода модального окна prompt.
    
    Args:
        text (str, optional): Текст для ввода в prompt. По умолчанию "text".
        
    Returns:
        None
        
    Описание:
        Функция вводит указанный текст в поле ввода модального окна типа prompt.
        Используется для заполнения пользовательского ввода в alert с текстовым полем.
    """
    alert.send_keys(text)


try:
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10, poll_frequency=1)
    driver.get("https://demoqa.com/alerts")

    # Вызываем появление кнопки для вызова первого алерта
    click_button(ALERT_1_BUTTON)
    # Ожидаем появление алерта
    alert = wait.until(EC.alert_is_present())
    # Переводим фокус на алерт
    focus_to_alert()
    # Проверяем текст первого Алерта
    assertAlertText("You clicked a button", 2)
    # Принимает алерт
    accept_alert()
    # save_screenshot(1)
    # Вызываем появление кнопки для вызова второго алерта

    click_button(ALERT_2_BUTTON)
    # Переводим фокус на алерт
    focus_to_alert()
    # Проверяем текст второго Алерта
    assertAlertText("This alert appeared after 5 seconds", 2)
    # Принимает алерт
    accept_alert()


    click_button(ALERT_3_BUTTON)
    # Переводим фокус на алерт
    focus_to_alert()
    # Проверяем текст второго Алерта
    assertAlertText("Do you confirm action?", 3)
    # Принимает алерт
    accept_alert()
    # Проверяем вывод текста после принятия алерта
    expectedText("//span[@id='confirmResult']", "You selected Ok")

    # Проверяем отмену алерта
    click_button(ALERT_3_BUTTON)
    # Переводим фокус на алерт
    focus_to_alert()
    # Проверяем текст второго Алерта
    assertAlertText("Do you confirm action?", 3)
    # Отмена алерта
    dismiss_alert()
    # Проверяем вывод текста после отмены алерта
    expectedText("//span[@id='confirmResult']", "You selected Cancel")


    # Проверяем отмену алерта
    click_button(ALERT_4_BUTTON)
    # Переводим фокус на алерт
    focus_to_alert()
    # Проверяем текст второго Алерта
    assertAlertText("Please enter your name", 4)
    # Вводим текст в поле алерта
    test_text = "test_text"
    send_keys_alert(test_text)
    
    # Принимает алерт
    accept_alert()
    # Проверяем вывод текста после принятия алерта
    expectedText("//span[@id='promptResult']", test_text)
    save_screenshot()


finally:
    driver.quit()