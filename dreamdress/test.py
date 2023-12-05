from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set the path to your ChromeDriver executable
chrome_driver_path = r'C:\Users\hp\OneDrive\Desktop\project\chromedriver.exe'

# Set up the Chrome service
chrome_service = Service(chrome_driver_path)

# Initialize the Chrome browser with the service
driver = webdriver.Chrome(service=chrome_service)

driver.implicitly_wait(10)


# Open the login page
driver.get('http://127.0.0.1:8000/registration/signin/')

# Find login elements and perform actions
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')
login_button = driver.find_element(By.NAME, 'submit')

username_input.send_keys('Rintu')
password_input.send_keys('Abc1234#')
login_button.click()

# Add assertions or other validation as needed
assert 'Rintu' in driver.page_source

# Close the browser
driver.quit()