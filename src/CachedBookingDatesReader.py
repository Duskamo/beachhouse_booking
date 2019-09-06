
import csv

class CachedBookingDatesReader:
	def __init__(self):
		self.bookingDates = []
		self.reservationsCSV = "data/CachedBookingDates.csv"

	def readBookingDates(self):	
		with open(self.reservationsCSV, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=":")
			for row in reader:
				self.bookingDates.append({
					"date":row[0],
					"availability":row[1]
				})

	def getBookingDates(self):
		return self.bookingDates
