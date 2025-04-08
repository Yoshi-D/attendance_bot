import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests
from captcha_reader import captcha_extraction
from otp_extraction import fetch_otp
from password import password_extraction


driverPath = "/Users/shamdhage/Desktop/new-brave-chromedriver-mac-x64/chromedriver" # Path to ChromeDriver
service = Service(driverPath)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" # Path to Brave Browser (this is the default)
driver = webdriver.Chrome(service=service, options= options)

url = "https://saral.iitjammu.ac.in/"
driver.get(url)
print("Opened saral")

driver.find_element("xpath",'//*[@id="submit"]').click()
driver.find_element("xpath",'//*[@id="ssubmit"]').click()

driver.find_element("xpath",'//*[@id="txt_luserid"]').send_keys("2023UMA0239")
driver.find_element("xpath",'//*[@id="txt_lpwd"]').send_keys(password_extraction("eg_password"))
print("Entered username and password")

captcha_element = driver.find_element(By.XPATH, '//img[@id="captchaimg"]')
captcha_url = captcha_element.get_attribute("src")

image_data = requests.get(captcha_url).content
with open("new_captcha.jpg", "wb") as file:
    file.write(image_data)
print("Downloaded captcha image")

print("Extracting text from image...")
captcha_text = captcha_extraction()
if not captcha_text:
    print("Captcha could not be solved")
else:
    print("Captcha solved: ",captcha_text)

input_field_captcha = driver.find_element("xpath",'//*[@id="cap"]')
input_field_captcha.send_keys(captcha_text)
driver.find_element("xpath",'//*[@id="submit"]').click()
time.sleep(3)

otp = fetch_otp()
if otp:
    print("OTP is",otp)

driver.find_element("xpath",'//*[@id="txt_ipotp"]').send_keys(otp)
driver.find_element("xpath", '//*[@id="ip_submit"]').click()
time.sleep(2)

iframe_list = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe_list[1])

div_element = driver.find_element(By.XPATH, "//div[text()='My Classroom Attendance (Student)']")
div_element.click()
time.sleep(0.9)

year = driver.find_element("xpath",'//*[@id="year"]')
dropdown = Select(year)
dropdown.select_by_visible_text("2024-25")
print("Selected year 2024-25")

sem = driver.find_element("xpath",'//*[@id="sem"]')
dropdown = Select(sem)
dropdown.select_by_visible_text("02")
print("Selected sem 02")

proceed = driver.find_element("xpath",'//*[@id="submit"]')
proceed.click()
time.sleep(1.5)

first_row = driver.find_element("xpath",'html/body/table/tbody/tr[1]')
classes = first_row.text.split(' ')[1:]

last_row = driver.find_element("xpath",'(//table/tbody/tr)[last()-1]')
attendance_percentage = last_row.text.split(' ')[3:]


dictionary = {}
for i in range(len(classes) - 3):
    dictionary[classes[i]] = attendance_percentage[i]
print("Attendance successfully retrieved")
print(dictionary)
driver.quit()


