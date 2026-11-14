import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
@pytest.mark.parametrize('a,op,b,expected', [
 ('2','+','3','5'),('7','-','10','-3'),('-4','*','2.5','-10'),
 ('9','/','2','4.5'),('0.1','+','0.2','0.3'),('0','*','5','0'),
 ('5','/','0','Ошибка: деление на ноль'),
 ('','+','2','Ошибка: введите два числа'),
 ('abc','+','2','Ошибка: введите два числа'),
])
def test_calculator(driver, base_url, a, op, b, expected):
 driver.get(base_url+'/calculator.html')
 driver.find_element(By.ID,'a').send_keys(a)
 Select(driver.find_element(By.ID,'op')).select_by_visible_text(op)
 driver.find_element(By.ID,'b').send_keys(b)
 driver.find_element(By.ID,'calculate').click()
 assert driver.find_element(By.ID,'result').text == expected
 if op=='/' and b=='0': driver.save_screenshot('evidence/lab01-zero.png')

def test_clear(driver, base_url):
 driver.get(base_url+'/calculator.html')
 driver.find_element(By.ID,'a').send_keys('2')
 driver.find_element(By.ID,'b').send_keys('3')
 driver.find_element(By.ID,'calculate').click()
 driver.find_element(By.ID,'clear').click()
 assert driver.find_element(By.ID,'a').get_attribute('value') == ''
 assert driver.find_element(By.ID,'b').get_attribute('value') == ''
 assert driver.find_element(By.ID,'result').text == ''
 assert driver.switch_to.active_element.get_attribute('id') == 'a'
 driver.save_screenshot('evidence/lab01-clear.png')
