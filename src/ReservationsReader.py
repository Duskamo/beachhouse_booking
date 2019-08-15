
import csv

class ReservationsReader:
	def __init__(self):
		self.bookedDates = []
		self.reservationsCSV = "data/Reservations.csv"

	def readBookedDates(self):	
		with open(self.reservationsCSV, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.bookedDates.append({
					"startDate":row['Check-in'],
					"endDate":row['Check-out']
				})

	def getBookedDates(self):
		return self.bookedDates
