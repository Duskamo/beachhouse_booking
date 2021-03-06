
from datetime import datetime, timedelta

class DateComparer:
	def __init__(self, bookedDates):
		self.bookedDates = bookedDates

	def isDateAvailable(self, bookingRequest):
		isDateAvailable = []

		bookingStart = datetime.strptime(bookingRequest["startDate"],"%m/%d/%Y")
		bookingEnd = datetime.strptime(bookingRequest["endDate"],"%m/%d/%Y")	
		
		bookingDateRange = self.generateDateRange(bookingStart,bookingEnd)

		for i in range(len(self.bookedDates)):
			for j in range(len(bookingDateRange)):
				bookedStart = datetime.strptime(self.bookedDates[i]["startDate"],"%Y-%m-%d")
				bookedEnd = datetime.strptime(self.bookedDates[i]["endDate"],"%Y-%m-%d")

				if (bookedStart <= bookingDateRange[j] <= bookedEnd or bookedStart <= bookingDateRange[j] <= bookedEnd):
					isDateAvailable.append(False)
				else:
					isDateAvailable.append(True)

		if (False in isDateAvailable):
			return False
		else:
			return True

	def generateDateRange(self,bookingStart,bookingEnd):
		date_list = [bookingStart + timedelta(days=x) for x in range((bookingEnd - bookingStart).days+1)]
		return date_list

	
	def isDateCurrent(self, bookingRequest):
		presentDate = datetime.now()
		startDate = datetime.strptime(bookingRequest["startDate"],"%m/%d/%Y")

		return startDate >= presentDate 

	def areDatesInOrder(self, bookingRequest):
		startDate = datetime.strptime(bookingRequest["startDate"],"%m/%d/%Y")
		endDate = datetime.strptime(bookingRequest["endDate"],"%m/%d/%Y")

		return startDate < endDate 
