
# test 1
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class LoginformTest(LiveServerTestCase):
#     def testloginpage(self):
#         driver = webdriver.Chrome()
#         driver.get('http://127.0.0.1:8000/registration/signin/')
#         time.sleep(5)
#         username_input = driver.find_element(By.NAME, 'username')
#         password_input = driver.find_element(By.NAME, 'password')
#         login_button = driver.find_element(By.NAME, 'submit')
#         username_input.send_keys('Riya')
#         password_input.send_keys('Riyasaji2001#')
#         login_button.send_keys(Keys.RETURN)
#         assert 'Riya' in driver.page_source
  
# TEST 2

# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class SellerLoginTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'Riya'
#         self.password = 'Riyasaji2001#'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/registration/signin/')
#         time.sleep(5)
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(5)  

#     def add_product(self):
#         self.login()

#         self.driver.get('http://127.0.0.1:8000/seller_dashboard/')
#         time.sleep(5)  

#         view_ad_product= self.driver.find_element(By.LINK_TEXT, 'Add Products')
#         view_ad_product.click()
#         time.sleep(5)  

#         button = self.driver.find_element(By.NAME, 'addproduct')
#         self.assertIsNotNone(button)

# Test 3


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'Riya'
        self.password = 'Riyasaji2001#'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/registration/signin/')
        time.sleep(5)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(5)  

    def test_doctor_booking(self):
        self.login()

        self.driver.get('http://127.0.0.1:8000/home/')
        time.sleep(5)  

        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
        view_doctors_button.click()
        time.sleep(5)  

        book_now_button = self.driver.find_element(By.LINK_TEXT, 'View Detail')
        book_now_button.click()
        time.sleep(5)  

        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
        self.assertIsNotNone(proceed_button)