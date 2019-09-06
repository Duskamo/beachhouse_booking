
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

from src.CachedBookingDatesReader import CachedBookingDatesReader 
from src.CachedBookingDatesWriter import CachedBookingDatesWriter 

class VRBOAutomator:
	def __init__(self):
		self.driver = None
		self.url = "https://www.vrbo.com/auth/vrbo/login?service=https%3A%2F%2Fwww.vrbo.com%2Fhaod%2Fauth%2Fsignin.html"

	# Reuseable functions
	def gotoVRBOHomePage(self):
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		#chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument("--window-size=1920,1080")
		chrome_options.add_argument('--start-maximized')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--proxy-server='direct://'")
		chrome_options.add_argument("--proxy-bypass-list=*")
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--ignore-certificate-errors')

		capabilities = DesiredCapabilities.CHROME.copy()
		capabilities['acceptSslCerts'] = True 
		capabilities['acceptInsecureCerts'] = True

		self.driver = webdriver.Chrome("/var/www/html/p35/dlandrybeachhouse_workspace/beachhouse_booking/libs/chromedriver",chrome_options=chrome_options, desired_capabilities=capabilities)
		self.enable_download_in_headless_chrome(self.driver,"/home/dustin/Downloads/")
		self.driver.get(self.url)

	def login(self, username, password):
		time.sleep(5)

		usernameField = self.driver.find_element_by_id("username")
		passwordField = self.driver.find_element_by_id("password")
		loginButton = self.driver.find_element_by_id("form-submit")

		usernameField.send_keys(username)
		passwordField.send_keys(password)
		loginButton.submit()

	def enable_download_in_headless_chrome(self, driver, download_dir):
		#add missing support for chrome "send_command"  to selenium webdriver
		driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

		params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
		driver.execute("send_command", params)

	# Get Reservation Automation
	def gotoVRBOCalendarPage(self):
		calendarUrl = "https://admin.vrbo.com/pxcalendars/reservations/321.1733517.2295019"
		self.driver.get(calendarUrl)	

	def exportCalendarCSV(self):
		time.sleep(20)
		
		exportDropDown = self.driver.find_element_by_id("reservation-import-export-dropdown")
		exportDropDown.click()

		exportButton = self.driver.find_element_by_xpath(".//div[@class='calendar-toolbar']/div/ul/li[3]")
		exportButton.click()

		exportAllCheckbox = self.driver.find_element_by_xpath(".//*[@class='calendar-v2-modal-body']/div[3]")
		exportAllCheckbox.click()

		exportSaveButton = self.driver.find_element_by_id("calendar-v2-modal-save-button")
		exportSaveButton.click()

		time.sleep(5)

		self.driver.close()
		
	def moveCalendarCSVToDataDirectory(self):
		time.sleep(10)

		sourceDirectory = "/home/dustin/Downloads/Reservations.csv"
		targetDirectory = "/var/www/html/p35/dlandrybeachhouse_workspace/beachhouse_booking/data/Reservations.csv"

		os.rename(sourceDirectory,targetDirectory)

	# Post Reservation Automation
	def gotoVRBOReservedListPage(self):
		reservedListUrl = "https://www.vrbo.com/rm/f-reservations/"
		self.driver.get(reservedListUrl)

		time.sleep(15)

	def reserveBookedDates(self, bookingInfo):
		addReservationButton = self.driver.find_element_by_id("add-reservation-button")
		addReservationButton.click()

		time.sleep(15)

		# add first and last name to reservation
		firstNameField = self.driver.find_element_by_id("guest.firstName")
		firstNameField.send_keys("Dustin")

		lastNameField = self.driver.find_element_by_id("guest.lastName")
		lastNameField.send_keys("Landry")

		# add start date to reservation
		self.driver.find_element_by_id('res-datepicker-start').click()
		self.addDateToDatePicker(bookingInfo['rentalInfo']['arrivalDate'])

		# add end date to reservation
		self.addDateToDatePicker(bookingInfo['rentalInfo']['departDate'])

		# select booked from status dropdown 
		statusDropdown = self.driver.find_element_by_xpath('.//select[@name="status"]/option[text()="Blocked"]')
		statusDropdown.click()

		# save reservation
		saveReservationButton = self.driver.find_element_by_id('save-reservation')
		saveReservationButton.click()	

		# close driver after reservation is booked
		self.driver.close()

	def addDateToDatePicker(self, bookedDate):
		# get month and year from calendar
		dpMonth = self.driver.find_element_by_class_name('ui-datepicker-month')
		dpYear = self.driver.find_element_by_class_name('ui-datepicker-year')
		dpHeader = dpMonth.text + " " + dpYear.text

		# check they match with the booked month and year, if not find the match
		bookedHeader = self.getBookedHeader(bookedDate)
		while (dpHeader != bookedHeader):
			# find the month that matches and iterate on GUI
			dpNextButton = self.driver.find_element_by_class_name('ui-datepicker-next')
			dpNextButton.click()

			dpMonth = self.driver.find_element_by_class_name('ui-datepicker-month')
			dpYear = self.driver.find_element_by_class_name('ui-datepicker-year')
			dpHeader = dpMonth.text + " " + dpYear.text

		# store all days in list and loop through them until the correct one is found
		dpDaysOfMonth = self.driver.find_elements_by_class_name("ui-state-default")
		for day in dpDaysOfMonth:
			if day.text == bookedDate[-2:]:
				day.click()
				break

	def getBookedHeader(self, bookedDate):
		# 2019-08-20, 08-20-2018
		monthDict = {
			"01": "January",
			"02": "February",
			"03": "March",
			"04": "April",
			"05": "May",
			"06": "June",
			"07": "July",
			"08": "August",
			"09": "September",
			"10": "October",
			"11": "November",
			"12": "December",
		}

		return monthDict[bookedDate[5:7]] + " " + bookedDate[0:4]

	# Check VRBO for changes in reservations
	def gotoVRBOOwnerPage(self):
		vrboOwnerPage = "https://vrbo.com/1733517"
		self.driver.get(vrboOwnerPage)

		time.sleep(10)

	def viewCalendarDates(self):
		calendarSectionButton = self.driver.find_element_by_xpath('.//div[@id="desktop-nav"]//ul/li[5]')
		calendarSectionButton.click()

		time.sleep(5)

	def scrapeAllDates(self):
		calendarDates = self.driver.find_elements_by_xpath('.//*[@id="rates-availability"]//td/div/div')
		self.calendarDatesAvailability = []
		
		for date in calendarDates:
			calendarName = date.find_element_by_xpath('../..')
			self.calendarDatesAvailability.append({'date':calendarName.get_attribute('aria-label'), 'availability':date.get_attribute('class')})

		self.driver.close()

	def checkForChangesInBooking(self):
		# Read in reservations cache from CachedBookingDates.csv file
		cachedBookingDatesReader = CachedBookingDatesReader()
		cachedBookingDatesReader.readBookingDates()
		bookingDates = cachedBookingDatesReader.getBookingDates()

		# Compare dates in cached file to current dates
		isBookingChanged = False
		for i in range(len(self.calendarDatesAvailability)):
			if self.calendarDatesAvailability[i]['availability'] != bookingDates[i]['availability']:
				isBookingChanged = True

		if isBookingChanged:
			# Update Cache
			cachedBookingDatesWriter = CachedBookingDatesWriter()
			cachedBookingDatesWriter.writeBookedDates(self.calendarDatesAvailability)

			return True
		else:
			return False

