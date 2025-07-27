from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    url = "https://the-internet.herokuapp.com/status_codes"
    driver.get(url)

    # находим все ссылки со статус-кодами по xpath, 
    # они внутри div[@class='example']//a, и текст — код статуса
    links_xpath = "//div[@class='example']//a[not(text()='here')]"
    
    # Получаем список текстов ссылок сначала (например, 200, 301 и т.п.)
    # чтобы избежать stale элемент при перезагрузке страницы
    links_texts = [el.text for el in driver.find_elements("xpath", links_xpath)]
    
    print(links_texts)

    for text in links_texts:
        # после каждого перехода на страницу со статусом возвращаемся
        # и снова находим ссылку с нужным текстом, кликаем
        driver.get(url)
        link = driver.find_element("xpath", f"//div[@class='example']//a[text()='{text}']")
        link.click()

        print(f"Перешли по ссылке со статусом {text}, URL: {driver.current_url}")
        driver.back()

finally:
    driver.quit()
