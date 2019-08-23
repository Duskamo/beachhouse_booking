
import mysql.connector

class BookingDatabase:
	def __init__(self):		
		self.mydb = None
		self.mycursor = None

	def connect(self):
		self.mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Sassy13",
			database="dlandrybeachhouses"
		)

		self.mycursor = self.mydb.cursor()

	def save(self,bookingInfo):	
		# contactInfo insert
		sql = "INSERT INTO ContactInfo (firstName, lastName, email, phone) VALUES (%s, %s, %s, %s);"
		val = (bookingInfo['contactInfo']['firstName'],bookingInfo['contactInfo']['lastName'],bookingInfo['contactInfo']['email'],bookingInfo['contactInfo']['phone'])
		self.mycursor.execute(sql, val)

		self.mydb.commit()

		# termsCB insert
		sql = "INSERT INTO TermsConditions (accepted) VALUES (%s);"
		val = (bookingInfo['termsCB'],)
		self.mycursor.execute(sql, val)

		self.mydb.commit()

		# paymentInfo insert
		sql = "INSERT INTO PaymentInfo (firstNameOnCard, lastNameOnCard, paymentAmount, receiptEmail) VALUES (%s, %s, %s, %s);"
		val = (bookingInfo['paymentInfo']['firstNameOnCard'],bookingInfo['paymentInfo']['lastNameOnCard'],bookingInfo['paymentInfo']['paymentAmount'],bookingInfo['paymentInfo']['receiptEmail'])
		self.mycursor.execute(sql, val)

		self.mydb.commit()

		# billingInfo insert
		sql = "INSERT INTO BillingInfo (street, country, city, state, zip) VALUES (%s, %s, %s, %s, %s);"
		val = (bookingInfo['billingInfo']['street'],bookingInfo['billingInfo']['country'],bookingInfo['billingInfo']['city'],bookingInfo['billingInfo']['state'],bookingInfo['billingInfo']['zip'],)
		self.mycursor.execute(sql, val)

		self.mydb.commit()
