from selenium.webdriver.common.by import By
from pages.base_page import BasePage
class ContactPage(BasePage):
    NAME = (By.ID, 'name')
    EMAIL = (By.ID, 'email')
    MESSAGE = (By.ID, 'message')
    SEND = (By.ID, 'send')
    ERROR = (By.ID, 'error')
    SUCCESS = (By.ID, 'success')
    def load(self):
        self.open('/contact.html')
    def submit(self, name, email, message):
        for locator, value in [(self.NAME, name), (self.EMAIL, email), (self.MESSAGE, message)]:
            self.fill(locator, value)
        self.click(self.SEND)
    @property
    def error(self):
        return self.find(self.ERROR).text
    @property
    def success(self):
        return self.find(self.SUCCESS).text
