from flask import Flask, request
import os
import json

from data.Config import Config
from src.VRBOCalendarAutomator import VRBOCalendarAutomator
from src.ReservationsReader import ReservationsReader
from src.DateComparer import DateComparer
from src.BookingDatabase import BookingDatabase

app = Flask(__name__)

# Data Requests
@app.route('/request_calendar_dates', methods=['GET']) # Dispatched on CRON Service
def request_calendar_dates():	
	# Goto VRBO site calendar page and export calendar csv to data folder
	calendarAutomator = VRBOCalendarAutomator()
	calendarAutomator.gotoVRBOHomePage()
	calendarAutomator.login(Config.username,Config.password)
	calendarAutomator.gotoVRBOCalendarPage()
	calendarAutomator.exportCalendarCSV()
	calendarAutomator.moveCalendarCSVToDataDirectory()
	
	# Read calendar csv file and store start and end booking dates in object 
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()
	
	# Return booking dates json object to client (Not sending back correct dates)
	return json.dumps(bookedDates)

@app.route('/get_calendar_dates', methods=['GET'])
def get_calendar_dates():	
	# Read calendar csv file and store start and end booking dates in object 
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()
	
	# Return booking dates json object to client (Not sending back correct dates)
	return json.dumps(bookedDates)

@app.route('/booking_availability', methods=['POST'])
def booking_availability():
	# Gather booking request data
	bookingInfo = request.json
	
	# Gather booked dates
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()

	# Check if dates are available to book
	dateComparer = DateComparer(bookedDates)
	isDateAvailable = dateComparer.isDateAvailable(bookingInfo)

	# If dates are available return available, if not return unavailable
	if isDateAvailable:
		return "available"
	else:
		return "unavailable"

@app.route('/save_booked_information', methods=['POST'])
def save_booked_information():
	# Gather booking request data
	bookingInfo = request.json
	
	# Save booked dates to mysql database
	database = BookingDatabase()
	database.connect()
	database.save(bookingInfo)

	# If dates are available return available, if not return unavailable
	return "200"


# Run app on 0.0.0.0:5002
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5002))
	app.run(host='0.0.0.0', port=port)
