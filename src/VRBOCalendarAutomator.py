
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class VRBOCalendarAutomator:
	def __init__(self):
		self.driver = None
		self.url = "https://www.vrbo.com/auth/vrbo/login?service=https%3A%2F%2Fwww.vrbo.com%2Fhaod%2Fauth%2Fsignin.html"

	def gotoVRBOHomePage(self):
		chrome_options = Options()
		#chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('--start-maximized')
		self.driver = webdriver.Chrome("/var/www/html/p35/dlandrybeachhouse_workspace/beachhouse_booking/libs/chromedriver",chrome_options=chrome_options)
		self.driver.get(self.url)

	def login(self, username, password):
		usernameField = self.driver.find_element_by_id("username")
		passwordField = self.driver.find_element_by_id("password")
		loginButton = self.driver.find_element_by_id("form-submit")

		usernameField.send_keys(username)
		passwordField.send_keys(password)
		loginButton.submit()

	def gotoVRBOCalendarPage(self):
		calendarUrl = "https://admin.vrbo.com/pxcalendars/reservations/321.1733517.2295019"
		self.driver.get(calendarUrl)	

	def exportCalendarCSV(self):
		self.driver.implicitly_wait(10)
		
		exportDropDown = self.driver.find_element_by_id("reservation-import-export-dropdown")
		exportDropDown.click()

		exportButton = self.driver.find_element_by_xpath(".//div[@class='calendar-toolbar']/div/ul/li[3]")
		exportButton.click()

		exportAllCheckbox = self.driver.find_element_by_xpath(".//*[@class='calendar-v2-modal-body']/div[3]")
		exportAllCheckbox.click()

		exportSaveButton = self.driver.find_element_by_id("calendar-v2-modal-save-button")
		exportSaveButton.click()

		self.driver.close()

	def moveCalendarCSVToDataDirectory(self):
		time.sleep(10)

		sourceDirectory = "/home/dustin/Downloads/Reservations.csv"
		targetDirectory = "/var/www/html/p35/dlandrybeachhouse_workspace/beachhouse_booking/data/Reservations.csv"

		os.rename(sourceDirectory,targetDirectory)




