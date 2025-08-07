from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options_list = ["--headless", "--incognito", "--window-size=1920,1080"]

def add_options(options, options_list):
    if not options_list:
        return options
    else:
        for option in options_list:
            options.add_argument(option)
    return options

options = add_options(options, options_list)
driver = webdriver.Chrome(service=service)

# Locators

button_business = ("xpath", "//a[@class='nav-link' and text()='For Business']")
button_start_free = ("xpath", "//div[text()='Start for Free']")

try:
    driver.get("https://hyperskill.org/")
    wait = WebDriverWait(driver, 30, 1)
    if platform.system() == "Darwin":
        wait.until(EC.element_to_be_clickable(button_business)).send_keys(Keys.COMMAND + Keys.RETURN)
    else:
        wait.until(EC.element_to_be_clickable(button_business)).send_keys(Keys.CONTROL + Keys.RETURN)
        

    open_tabs = driver.window_handles
    print(open_tabs)
    driver.switch_to.window(open_tabs[1])
    wait.until(EC.element_to_be_clickable(button_start_free))
    driver.save_screenshot("test.png")
finally:
    driver.quit()