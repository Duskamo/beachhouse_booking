from datetime import datetime, timedelta
import csv
from src.DateComparer import DateComparer

class RatesReader:
	def __init__(self):
		self.bookingRates = []
		self.ratesCSV = "data/Rates.csv"

	def readRates(self):
		with open(self.ratesCSV, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.bookingRates.append({
					"date":row['date'],
					"rate":row['rate']
				})

	def removeBookedDates(self,bookedDates):
		# Generate Range of all booked dates (Setup)
		totalBookedRanges = []
		totalBookedDates = []
		dateComparer = DateComparer(bookedDates)
			
		# Generate all date ranges and store each range in totalBookedRanges
		for i in range(len(bookedDates)):	
			totalBookedRanges.append(dateComparer.generateDateRange(datetime.strptime(bookedDates[i]["startDate"],"%m/%d/%Y"), datetime.strptime(bookedDates[i]["endDate"],"%m/%d/%Y")))
		
		# Store all dates in a 1-demenstional list to loop through easier when removing dates from bookingRates
		for i in range(len(totalBookedRanges)):
			for j in range(len(totalBookedRanges[i])):
				totalBookedDates.append(totalBookedRanges[i][j])

		# Remove all booked dates from bookingRates list
		bookedRates = [bookedRate for bookedRate in self.bookingRates for bookedDate in totalBookedDates if bookedRate['date'] == bookedDate.strftime("%m/%d")]

		for rate in bookedRates:
			self.bookingRates.remove(rate)
		
	def getRates(self):
		return self.bookingRates
