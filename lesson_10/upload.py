import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path="/usr/local/bin/chromedriver")
options = Options()

driver = webdriver.Chrome(service=service, options=options)

try:
    input_file = "//input[@id='file-upload']"
    driver.get("https://the-internet.herokuapp.com/upload")
    time.sleep(5)
    driver.find_element("xpath", input_file).send_keys(os.path.join(os.getcwd()), "downloads/images.jpeg")
    
    time.sleep(5)
finally:
    driver.quit()

    