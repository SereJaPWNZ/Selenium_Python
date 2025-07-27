import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")


# LOCATOR
EMAIL_FIELD = ("xpath", "//input[@id='userEmail']")
SUBMIT = ("xpath", "//button[@id='submit']")

try:
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://demoqa.com/text-box")
    wait.until(EC.visibility_of_element_located(EMAIL_FIELD)).send_keys("fdsdsffd@test.com")
    time.sleep(5)
    driver.save_screenshot("test.png")
    wait.until(EC.visibility_of_element_located(SUBMIT)).click()
    driver.save_screenshot("test1.png")

finally:
    driver.quit()