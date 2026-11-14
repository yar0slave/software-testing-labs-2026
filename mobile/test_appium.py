"""Appium tests on Android 15. Requires a running Appium server."""
import os
import subprocess
from pathlib import Path
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
PKG = 'ru.grinko.labnotes'
@pytest.fixture
def mobile():
    options = UiAutomator2Options().load_capabilities({
        'platformName': 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'LabEmulator',
        'appium:app': str(Path(__file__).with_name('lab-notes.apk').resolve()),
        'appium:appPackage': PKG,
        'appium:appActivity': '.MainActivity',
        'appium:noReset': False,
        'appium:newCommandTimeout': 120,
    })
    driver = webdriver.Remote(os.getenv('APPIUM_URL','http://127.0.0.1:4723'), options=options)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID,'note-input')))
    yield driver
    driver.quit()

def find(driver, name):
    return driver.find_element(AppiumBy.ACCESSIBILITY_ID,name)

def add(driver,text):
    find(driver,'note-input').send_keys(text)
    find(driver,'add-note').click()
    if driver.is_keyboard_shown(): driver.hide_keyboard()

def test_add_note(mobile):
    add(mobile,'Appium test')
    assert find(mobile,'note-0').text == 'Appium test'
    mobile.save_screenshot('evidence/lab07-appium.png')

def test_empty_note(mobile):
    find(mobile,'add-note').click()
    assert not mobile.find_elements(AppiumBy.ACCESSIBILITY_ID,'note-0')
    mobile.save_screenshot('evidence/lab07-empty.png')

def test_rotation_preserves_note_and_draft(mobile):
    add(mobile,'Saved note')
    find(mobile,'note-input').send_keys('Draft')
    if mobile.is_keyboard_shown(): mobile.hide_keyboard()
    mobile.orientation='LANDSCAPE'
    assert find(mobile,'note-0').text == 'Saved note'
    assert find(mobile,'note-input').text == 'Draft'
    mobile.save_screenshot('evidence/lab07-landscape.png')
    mobile.orientation='PORTRAIT'
    assert find(mobile,'note-input').text == 'Draft'

def test_restart_preserves_saved_note(mobile):
    add(mobile,'Persistent')
    mobile.terminate_app(PKG)
    mobile.activate_app(PKG)
    assert find(mobile,'note-0').text == 'Persistent'

def test_swipe_delete(mobile):
    add(mobile,'Delete me')
    rect=find(mobile,'note-0').rect
    y=rect['y']+rect['height']//2
    mobile.swipe(rect['x']+rect['width']-10,y,rect['x']+10,y,500)
    assert not mobile.find_elements(AppiumBy.ACCESSIBILITY_ID,'note-0')

def test_sms_interruption(mobile):
    add(mobile,'Before SMS')
    subprocess.run(['adb','emu','sms','send','5551234','Lab test'],check=True)
    mobile.activate_app(PKG)
    assert find(mobile,'note-0').text == 'Before SMS'

def test_call_interruption(mobile):
    add(mobile,'Before call')
    try:
        subprocess.run(['adb','emu','gsm','call','5551234'],check=True)
        subprocess.run(['adb','emu','gsm','list'],check=True)
    finally:
        subprocess.run(['adb','emu','gsm','cancel','5551234'],check=True)
    mobile.activate_app(PKG)
    assert find(mobile,'note-0').text == 'Before call'

def test_repeated_add_and_clear(mobile):
    for i in range(10): add(mobile,'Note '+str(i))
    subprocess.run(['adb','shell','dumpsys','meminfo',PKG],check=True,
                   stdout=open('evidence/lab07-memory.txt','w'))
    find(mobile,'clear-notes').click()
    assert not mobile.find_elements(AppiumBy.ACCESSIBILITY_ID,'note-0')
    add(mobile,'After clear')
    assert find(mobile,'note-0').text == 'After clear'
