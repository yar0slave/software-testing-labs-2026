import pytest
from selenium.webdriver.common.by import By

def add(driver,text):
 driver.find_element(By.ID,'task').send_keys(text)
 driver.find_element(By.ID,'add').click()

@pytest.mark.parametrize('fixed',[False,True])
@pytest.mark.parametrize('scenario',['empty','delete','reload'])
def test_known_defects(driver,base_url,fixed,scenario):
 driver.get(base_url+'/todo.html'+('?fixed=1' if fixed else ''))
 if scenario=='empty':
  add(driver,'   ')
  actual=len(driver.find_elements(By.CSS_SELECTOR,'li'))
  expected=0
 elif scenario=='delete':
  add(driver,'Первая');add(driver,'Вторая')
  driver.find_elements(By.CSS_SELECTOR,'li button')[1].click()
  actual=[e.text for e in driver.find_elements(By.CSS_SELECTOR,'li span')]
  expected=['Первая']
 else:
  add(driver,'Сохранённая заметка');driver.refresh()
  actual=[e.text for e in driver.find_elements(By.CSS_SELECTOR,'li span')]
  expected=['Сохранённая заметка']
 driver.save_screenshot(f'evidence/lab02-{scenario}-{"fixed" if fixed else "bug"}.png')
 if not fixed:
  assert actual!=expected, 'Учебный дефект неожиданно исчез'
 else:
  assert actual==expected
