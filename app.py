from flask import Flask, request
import os
import json

from data.Config import Config
from src.VRBOCalendarAutomator import VRBOCalendarAutomator
from src.ReservationsReader import ReservationsReader

app = Flask(__name__)

# Data Requests
@app.route('/get_calendar_dates', methods=['GET'])
def get_calendar_dates():	
	# Goto VRBO site calendar page and export calendar csv to data folder
	"""
	calendarAutomator = VRBOCalendarAutomator()
	calendarAutomator.gotoVRBOHomePage()
	calendarAutomator.login(Config.username,Config.password)
	calendarAutomator.gotoVRBOCalendarPage()
	calendarAutomator.exportCalendarCSV()
	calendarAutomator.moveCalendarCSVToDataDirectory()
	"""
	# Read calendar csv file and store start and end booking dates in object 
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()
	
	# Return booking dates json object to client (Not sending back correct dates)
	return json.dumps(bookedDates)

@app.route('/booking_index', methods=['POST'])
def booking_index():
	# Gather Data
	bookingInfo = request.json
	
	# Check if dates are available to book
	print(bookingInfo['startDate'])

	# Return user to booking page with dates pre-booked if available, if not then return error message to user
	return "200"


# Run app on 0.0.0.0:5002
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5002))
	app.run(host='0.0.0.0', port=port)
