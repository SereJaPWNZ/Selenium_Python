from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# --- Настройка Chrome под Windows 11 десктоп ---
def create_driver():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument(f"user-agent={user_agent}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Удаление следов Selenium
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })

    driver.set_window_size(1920, 1080)
    return driver


# --- Логика работы со страницей ---
def click_element(locator):
    try:
        wait.until(EC.element_to_be_clickable(locator)).click()
    except TimeoutException:
        print(f"Не удалось кликнуть: {locator}")


def status_element(element, index):
    try:
        cls = element.get_attribute("class")
        if "active" in cls:
            print(f"#{index + 1}: Статус активен")
        else:
            print(f"#{index + 1}: Не активен")
    except Exception as e:
        print(f"Ошибка статуса #{index + 1}: {e}")


# --- Основной блок ---
GRID_TAB_LOCATOR = ("xpath", "//a[@class='nav-item nav-link']")
ELEMENTS_GRID_TAB_LOCATOR = ("xpath", "//div[@id='gridContainer']//li[contains(@class, 'list-group-item')]")

try:
    driver = create_driver()
    wait = WebDriverWait(driver, 20, 0.5)

    driver.get("https://demoqa.com/selectable")

    click_element(GRID_TAB_LOCATOR)

    elements = driver.find_elements(*ELEMENTS_GRID_TAB_LOCATOR)

    # Статусы до клика
    for i, el in enumerate(elements):
        status_element(el, i)

    # Кликаем по каждому элементу
    for i, el in enumerate(elements):
        try:
            el.click()
            print(f"Clicked #{i + 1}")
        except ElementClickInterceptedException:
            print(f"⚠️ Не удалось кликнуть #{i + 1}")

    # Статусы после клика
    for i, el in enumerate(elements):
        status_element(el, i)

finally:
    driver.quit()
