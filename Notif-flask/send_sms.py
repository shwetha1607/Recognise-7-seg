import urllib.request
import urllib.parse
from config import TextLocal

class SendSMS:
	def __init__(self):
		self.smsObj = TextLocal()
		self.apiKey = self.smsObj.apiKey
		
	def sendSMS(self, numbers, message):
	    data = urllib.parse.urlencode({'apikey': self.apiKey, 'numbers': numbers,
	                                   'message': message, 'test': True})
	    data = data.encode('utf-8')
	    print('Attempt to send')
	    request = urllib.request.Request("https://api.textlocal.in/send/?")
	    f = urllib.request.urlopen(request, data)
	    fr = f.read()
	    print(fr)


#resp = sendSMS('919742223577', 'This is your message')
#print(resp)