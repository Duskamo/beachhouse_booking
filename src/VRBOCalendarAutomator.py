
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
		""		

	def exportCalendarCSV(self):
		""

	def moveCalendarCSVToDataDirectory(self):
		""
