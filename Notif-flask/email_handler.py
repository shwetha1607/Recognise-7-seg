import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from config import Email

class ClassEmail:

	def __init__(self):
		self.emailObj = Email()
		self.session = smtplib.SMTP_SSL(self.emailObj.SMTP_SERVER, self.emailObj.SMTP_PORT)
		self.session.ehlo()
		self.session.login(self.emailObj.USERNAME, self.emailObj.PASSWORD)

	def initialise_Mail_Body(self, To_Add, Subject):
	    #Prepare Mail Body
		Mail_Body = MIMEMultipart()
		Mail_Body['From'] = self.emailObj.FROM_ADD
		Mail_Body['To'] = To_Add
		Mail_Body['Subject'] = Subject
		return Mail_Body

	def send_Image_Mail(self, To_Add, Subject, txtMessage, ImgFileName):
	    img_data = open(ImgFileName, 'rb').read()
	    Mail_Body = self.initialise_Mail_Body(To_Add, Subject)
	    Mail_Msg = MIMEText(txtMessage)
	    Mail_Body.attach(Mail_Msg)
	    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
	    Mail_Body.attach(image)
	    self.session.sendmail(self.emailObj.FROM_ADD, [To_Add], Mail_Body.as_string())


	def __del__(self):
	    self.session.close()
	    del self.session