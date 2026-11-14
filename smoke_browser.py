from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
try:
    driver.get('http://127.0.0.1:8765/login.html')
    print(driver.title)
finally:
    driver.quit()
