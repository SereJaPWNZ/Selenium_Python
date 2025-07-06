from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep


service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
options.add_argument("--incognito")

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://hyperskill.org/tracks")
    sleep(2)
    driver.find_elements("xpath", "//a[@class='nav-link']")[1].click()
    sleep(2)
finally:
    driver.quit()
