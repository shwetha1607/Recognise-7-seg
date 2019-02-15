from twilio.rest import Client
from config import Twilio

class SendWhatsApp:

	def __init__(self):
		self.waObj = Twilio()
		account_sid = self.waObj.account_sid
		auth_token = self.waObj.auth_token
		self.client = Client(account_sid, auth_token)
		self.sandboxNum = self.waObj.sandboxNum

	def sendText(self, numbers, messageBody):

		message = self.client.messages.create(
			body=messageBody,
			from_= self.sandboxNum,
            to='whatsapp:+919742223577'
        )

		print(message.sid)
