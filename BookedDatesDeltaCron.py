import requests
from src.VRBOAutomator import VRBOAutomator

def booked_dates_delta():	
	# Goto VRBO site, on owner page check for updated reservations
	vrboAutomator = VRBOAutomator()
	vrboAutomator.gotoVRBOHomePage()
	vrboAutomator.gotoVRBOOwnerPage()
	vrboAutomator.viewCalendarDates()
	vrboAutomator.scrapeAllDates()
	isBookingChanged = vrboAutomator.checkForChangesInBooking() 

	# Call get_reserved_dates endpoint to get new calendar information for GUI
	print("True " if isBookingChanged else "False")
	if isBookingChanged:
		bookingDatesServiceUrl = "http://localhost:5002/request_calendar_dates"
		bookingDates = requests.get(bookingDatesServiceUrl)
	
	return isBookingChanged

if __name__ == "__main__":
	booked_dates_delta()
