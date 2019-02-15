from email_handler import ClassEmail

class SendEmail:
	def __init__(self):
		self.email = ClassEmail()

	def sendMail(self, to_add, subject, message, imgfile):
		self.email.send_Image_Mail(to_add, subject, message, imgfile)
		del self.email