import csv

class CachedBookingDatesWriter:
	def __init__(self):
		self.reservationsCSV = "data/CachedBookingDates.csv"

	def writeBookedDates(self, bookingDates):	
		with open(self.reservationsCSV, 'w', newline='') as csvfile:
		    writer = csv.writer(csvfile, delimiter=':')

		    for date in bookingDates:
		    	writer.writerow([date['date'],date['availability']])

