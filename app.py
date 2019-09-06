from flask import Flask, request
import os
import json

from data.Config import Config
from src.VRBOAutomator import VRBOAutomator
from src.ReservationsReader import ReservationsReader
from src.ReservationsWriter import ReservationsWriter
from src.RatesReader import RatesReader
from src.DateComparer import DateComparer
from src.BookingDatabase import BookingDatabase

app = Flask(__name__)

# Data Requests
@app.route('/request_calendar_dates', methods=['GET']) # Dispatched on CRON Service callback
def request_calendar_dates():	
	# Goto VRBO site calendar page and export calendar csv to data folder
	vrboAutomator = VRBOAutomator()
	vrboAutomator.gotoVRBOHomePage()
	vrboAutomator.login(Config.username,Config.password)
	vrboAutomator.gotoVRBOCalendarPage()
	vrboAutomator.exportCalendarCSV()
	vrboAutomator.moveCalendarCSVToDataDirectory()
	
	return "200"

@app.route('/get_reserved_dates', methods=['GET'])
def get_reserved_dates():	
	# Read calendar csv file and store start and end booking dates in object 
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()
	
	# Return booking dates json object to client (Not sending back correct dates)
	return json.dumps(bookedDates)

@app.route('/get_rates_by_date', methods=['GET'])
def get_rates_by_date():	
	# Read calendar csv file and store start and end booking dates in object 
	reservationsReader = ReservationsReader()
	reservationsReader.readBookedDates()
	bookedDates = reservationsReader.getBookedDates()

	# Read dates and rates that are not yet booked
	ratesReader = RatesReader()
	ratesReader.readRates()
	ratesReader.removeBookedDates(bookedDates)
	bookingRates = ratesReader.getRates()
	
	# Return booking dates json object to client (Not sending back correct dates)
	return json.dumps(bookingRates)

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

@app.route('/save_booked_information_to_database', methods=['POST'])
def save_booked_information_to_database():
	# Gather booking request data
	bookingInfo = request.json
	
	# Save booked dates to mysql database
	database = BookingDatabase()
	database.connect()
	database.save(bookingInfo)

	# If dates are available return available, if not return unavailable
	return "200"

@app.route('/save_booked_information_to_reservations', methods=['POST'])
def save_booked_information_to_reservations():
	# Gather booking request data
	bookingInfo = request.json
	
	# Save booked dates to mysql database
	reservationsWriter = ReservationsWriter()
	reservationsWriter.writeBookedDates(bookingInfo)

	# Return Status Code
	return "200"

@app.route('/send_booked_information_to_vrbo', methods=['POST'])
def send_booked_information_to_vrbo():
	# Gather booking request data
	bookingInfo = request.json
	
	# Send booked dates to VRBO
	vrboAutomator = VRBOAutomator()
	vrboAutomator.gotoVRBOHomePage()
	vrboAutomator.login(Config.username,Config.password)
	vrboAutomator.gotoVRBOReservedListPage()
	vrboAutomator.reserveBookedDates(bookingInfo)

	# Return Status Code
	return "200"

# Run app on 0.0.0.0:5002
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5002))
	app.run(host='0.0.0.0', port=port)
