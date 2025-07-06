from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep


service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
# options.add_argument("--incognito")
# # options.add_argument("--start-maximized")


try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://testautomationpractice.blogspot.com/")
    sleep(3)
    WIKI_CLASS = driver.find_element("xpath", "//a[@class='wikipedia-search-wiki-link']")
    WIKI_SEARCH_ID = driver.find_element("xpath", "//input[@class='wikipedia-search-input']")
    WIKI_SEARCH_ICON = driver.find_element("xpath", "//input[@class='wikipedia-search-button']")
    DESCRIPTION = driver.find_element("xpath", "//span[1]")
    print("WIKI_CLASS", WIKI_CLASS.tag_name)
    print("WIKI_SEARCH_ID", WIKI_SEARCH_ID.tag_name)
    print("WIKI_SEARCH_ICON", WIKI_SEARCH_ICON.tag_name)
    print("DESCRIPTION", DESCRIPTION.tag_name)
finally:
    driver.quit()