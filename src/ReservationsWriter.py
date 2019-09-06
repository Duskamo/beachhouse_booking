import csv

class ReservationsWriter:
	def __init__(self):
		self.reservationsCSV = "data/Reservations.csv"

	def writeBookedDates(self, bookingInfo):	
		with open(self.reservationsCSV, 'a', newline='') as csvfile:
		    writer = csv.writer(csvfile)

		    writer.writerow(['9999','9999','Dena Landry Beach House','8/13/2019','denalandry@gmail.com','dena landry','337-257-6581',bookingInfo['rentalInfo']['arrivalDate'],bookingInfo['rentalInfo']['departDate'],'5','3','3','Booked','VRBO'])

