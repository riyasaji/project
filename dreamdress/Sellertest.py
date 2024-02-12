from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class LoginformTest(LiveServerTestCase):

    def testloginpage(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/registration/signin/')
        time.sleep(5)
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
        username_input.send_keys('Rintu')
        password_input.send_keys('Abc1234#')
        login_button.send_keys(Keys.RETURN)

        assert 'Rintu' in driver.page_source