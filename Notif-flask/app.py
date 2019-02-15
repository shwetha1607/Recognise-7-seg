from flask import Flask, render_template, request
from send_mail import SendEmail
from send_sms import SendSMS
from send_whatsapp import SendWhatsApp

app = Flask(__name__)

@app.route("/")
def main():
	return render_template("options.html")

@app.route("/email", methods=['POST', 'GET'])
def email():
	objE = SendEmail()
	#get mailID
	if request.method == 'POST':
		to_add = request.form.get("emailID")
		objE.sendMail(to_add, 'Temperature Alert', 'The display reads:', 'static/ledNumber4.jpg')
	return "Email sent"

@app.route("/sms", methods=['POST', 'GET'])
def sms():
	objS = SendSMS()
	# get number
	if request.method == 'POST':
		number = request.form.get("smsNum")
		objS.sendSMS(number, 'This is a test sms')
	return "SMS sent"

@app.route("/whatsapp", methods=['POST', 'GET'])
def whatsapp():
	objW = SendWhatsApp()
	# get number
	if request.method == 'POST':
		wnumber = request.form.get("WhatsappNum")
		objW.sendText(wnumber, 'This is a test whatsapp message')
	return "Text sent"

if __name__ == "__main__":
	app.run(host='localhost', port=5000, debug=True)
