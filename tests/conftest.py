import json
import os
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,900')
    options.add_argument('--no-sandbox')
    binary = os.getenv('CHROME_BINARY')
    if binary:
        options.binary_location = binary
    path = os.getenv('CHROMEDRIVER')
    remote = os.getenv('SELENIUM_URL')
    browser = (webdriver.Remote(command_executor=remote, options=options) if remote
               else webdriver.Chrome(service=Service(path) if path else Service(), options=options))
    Path('evidence').mkdir(exist_ok=True)
    Path('evidence/browser.json').write_text(json.dumps(browser.capabilities, indent=2))
    yield browser
    browser.quit()
@pytest.fixture
def base_url():
    return os.getenv('BASE_URL', 'http://127.0.0.1:8765')
