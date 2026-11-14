from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_valid_login(driver, base_url):
    driver.get(base_url + '/login.html')
    driver.find_element(By.ID, 'username').send_keys('student')
    driver.find_element(By.ID, 'password').send_keys('Test123!')
    driver.find_element(By.ID, 'submit').click()
    logout = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'logout')))
    assert logout.text == 'Logout'
    assert driver.find_element(By.ID, 'welcome').text == 'Вход выполнен'
    driver.save_screenshot('evidence/lab03-login.png')
    logout.click()
    assert driver.find_element(By.ID, 'login').is_displayed()

def test_invalid_login(driver, base_url):
    driver.get(base_url + '/login.html')
    driver.find_element(By.ID, 'username').send_keys('student')
    driver.find_element(By.ID, 'password').send_keys('wrong')
    driver.find_element(By.ID, 'submit').click()
    assert driver.find_element(By.ID, 'error').text == 'Неверный логин или пароль'
    assert not driver.find_element(By.ID, 'account').is_displayed()
