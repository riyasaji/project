
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


# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class DoctorBookingTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'Riya'
#         self.password = 'Riyasaji2001#'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/registration/signin/')
#         time.sleep(5)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(5)  

#     def test_doctor_booking(self):
#         self.login()

#         self.driver.get('http://127.0.0.1:8000/home/')
#         time.sleep(5)  

#         view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
#         view_doctors_button.click()
#         time.sleep(5)  

#         book_now_button = self.driver.find_element(By.LINK_TEXT, 'View Detail')
#         book_now_button.click()
#         time.sleep(5)  

#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
#         self.assertIsNotNone(proceed_button)



# # test1-main
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class LoginformTest(LiveServerTestCase):

#     def testloginpage(self):
#         driver = webdriver.Chrome()

#         driver.get('http://127.0.0.1:8000/signin/')
#         time.sleep(5)
#         username_input = driver.find_element(By.NAME, 'username')
#         password_input = driver.find_element(By.NAME, 'password')
#         login_button = driver.find_element(By.NAME, 'submit')
#         username_input.send_keys('rintu@gmail.com')
#         password_input.send_keys('Abc1234#')
#         login_button.send_keys(Keys.RETURN)

#         assert 'Tailor Dashboard!' in driver.page_source


#Test 2 - Customer+Shop+View DEtail
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class ViewDoctorTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jomolmariajohnson2024b@gmail.com'
#         self.password = 'Abc1234#'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/signin/')
#         time.sleep(5)
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(5)  

#     def test_doctor_booking(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/home/')
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
#         view_doctors_button.click()
#         time.sleep(3)  

#         # Step 4: Click on "Book Now" button
#         book_now_button = self.driver.find_element(By.LINK_TEXT, 'View Detail')
#         book_now_button.click()
#         time.sleep(3)  

#         # Step 5: Verify if "Proceed" button is present on the booking page
#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'Home')
#         self.assertIsNotNone(proceed_button)






# Test 3: Seller dashboart + update stock
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class DoctorBookingTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'amal@gmail.com'
        self.password = 'Abc1234#'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/signin/')
        time.sleep(3)
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(3)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/seller_dashboard/')
        time.sleep(3)  

        # Step 3: Click on "View Doctors" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'ManageStocks')
        view_doctors_button.click()
        time.sleep(3)  

        # Step 4: Click on "Book Now" button
        book_now_button = self.driver.find_element(By.LINK_TEXT, 'Update Stock')
        book_now_button.click()
        time.sleep(3)  


       # Step 5: Select slot from the dropdown
        input_field = self.driver.find_element(By.NAME, 'quantity')
        input_field.clear()
        input_field.send_keys('15') 
        time.sleep(3)

        # Step 6: Click on "Proceed" button
        proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Update"]')
        proceed_button.click()
        time.sleep(3)
        # Step 7: Verify if "Proceed" button is present on the booking page
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'Home')
        self.assertIsNotNone(proceed_button)


# Test 4
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class DoctorBookingTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jomolmariajohnson2024b@gmail.com'
#         self.password = 'Abc1234#'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/signin/')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_doctor_booking(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/home/')
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
#         view_doctors_button.click()
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'Shop')
#         view_doctors_button.click()
#         time.sleep(3)  

#         # Step 4: Click on "Book Now" button
#         book_now_button = self.driver.find_element(By.LINK_TEXT, 'View Detail')
#         book_now_button.click()
#         time.sleep(3)  
 
#         # Assuming 'self.driver' is your WebDriver instance

#         # Iterate over sizes and click on the corresponding radio button
#         sizes = self.driver.find_elements(By.NAME, 'size')
#         for size in sizes:
#             if size.get_attribute('value') == 'desired_size_value':
#                 size.click()  # Click on the radio button for the desired size
#                 break  # No need to continue once the desired size is selected

#         # Iterate over colors and click on the corresponding radio button
#         colors = self.driver.find_elements(By.NAME, 'color')
#         for color in colors:
#             if color.get_attribute('value') == 'desired_color_value':
#                 color.click()  # Click on the radio button for the desired color
#                 break  # No need to continue once the desired color is selected

#         # Input the desired quantity
#         quantity_input = self.driver.find_element(By.NAME, 'quantity')
#         quantity_input.clear()  # Clear any existing value
#         desired_quantity = 5  # Replace 5 with your desired quantity
#         quantity_input.send_keys(str(desired_quantity)) 

#         # Submit the form
#         # submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
#         # submit_button.click()

#         add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Add to Cart"]')
#         add_to_cart_button.click()
#         time.sleep(3)

#         # Step 7: Verify if "Proceed" button is present on the booking page
#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'Proceed to Checkout')
#         self.assertIsNotNone(proceed_button)

# Test 4: Doctor approving appointment
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class DoctorApprovalTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jeevaragnp2024b@mca.ajce.in'
#         self.password = 'jeeva@123'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/user_login/')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_doctor_booking(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/doctor_dashboard/')
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view_booking = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Approve"]')
#         view_booking.click()
#         time.sleep(3)  

        
#         # Step 4: 
#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'Reschedule')
#         self.assertIsNotNone(proceed_button)




# # Test 5: Doctor adding slot

# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class DoctorAddSlotTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jennyjohnson2024b@mca.ajce.in'
#         self.password = 'jenny@123'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/user_login/')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_doctor_booking(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/doctor_dashboard/')
#         time.sleep(3)  


#         schedule_timings_button = self.driver.find_element(By.LINK_TEXT, 'Schedule Timings')
#         schedule_timings_button.click()
#         time.sleep(3)

#         # Step 6: Fill and submit the form
#         date_input = self.driver.find_element(By.ID, 'date')
#         date_input.clear()  
#         date_input.send_keys('06-04-2024')  

#         # Select checkboxes by their IDs
#         checkboxes = ['slot1', 'slot2', 'slot3']  
#         for checkbox_id in checkboxes:
#             checkbox = self.driver.find_element(By.ID, checkbox_id)
#             if not checkbox.is_selected():
#                 checkbox.click()

#         # Click on the "Add" button
#         add_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Add"]')
#         add_button.click()
#         time.sleep(3)

#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'Timings')
#         self.assertIsNotNone(proceed_button)
