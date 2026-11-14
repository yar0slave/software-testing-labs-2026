import pytest
from pages.contact_page import ContactPage
@pytest.mark.parametrize('name_ok,email_ok,message_ok', [
    (True, True, True), (True, True, False),
    (True, False, True), (True, False, False),
    (False, True, True), (False, True, False),
    (False, False, True), (False, False, False),
])
def test_decision_table(driver, base_url, name_ok, email_ok, message_ok):
    page = ContactPage(driver, base_url)
    page.load()
    page.submit('Ярослав' if name_ok else '',
                'student@example.com' if email_ok else 'invalid',
                'Тестовое сообщение' if message_ok else '')
    if name_ok and email_ok and message_ok:
        assert page.success == 'Сообщение отправлено'
        assert driver.find_element(*page.ERROR).text == ''
        driver.save_screenshot('evidence/lab04-success.png')
    else:
        expected = []
        if not name_ok: expected.append('Введите имя')
        if not email_ok: expected.append('Введите корректный email')
        if not message_ok: expected.append('Введите сообщение')
        assert page.error == '; '.join(expected)
        assert driver.find_element(*page.SUCCESS).text == ''
        if not name_ok and email_ok and message_ok:
            driver.save_screenshot('evidence/lab04-error.png')
