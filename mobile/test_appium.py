"""Run after Appium server and emulator have started."""
import os
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_add_note():
    options = UiAutomator2Options().load_capabilities({
        'platformName': 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'LabEmulator',
        'appium:app': str(Path(__file__).with_name('lab-notes.apk').resolve()),
        'appium:appPackage': 'ru.grinko.labnotes',
        'appium:appActivity': '.MainActivity',
        'appium:noReset': False,
    })
    driver = webdriver.Remote(os.getenv('APPIUM_URL','http://127.0.0.1:4723'), options=options)
    try:
        wait = WebDriverWait(driver, 20)
        field = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'note-input')))
        field.send_keys('Проверка Appium')
        driver.find_element(AppiumBy.ACCESSIBILITY_ID,'add-note').click()
        note = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,'note-0')))
        assert note.text == 'Проверка Appium'
        driver.save_screenshot('evidence/lab07-appium.png')
    finally:
        driver.quit()
