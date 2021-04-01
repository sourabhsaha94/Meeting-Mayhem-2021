import time
import json
from flask import Flask
from flask import render_template, url_for, flash, redirect, request, session
from requests.models import Response
from venv import DB_MM


app = Flask(__name__)

@app.route('/time')
def get_current_time():
	return {'time': time.time()}

@app.route('/login',methods=["POST"])
def get_current():
	print("inside login")
	loginInfo = json.loads(request.data)
	user = loginInfo['email']
	pwd = loginInfo['password']

	loginExists = True
	#loginExists = DB_MM.checkUserLogin(user, pwd)
	print("  testing login:",loginExists)

	responseObject = {}
	responseObject['URI'] = '1234';

	print("",flush=True)
	return responseObject, 200

@app.route('/sendmessage',methods=["POST"])
def send_message():

	print("inside send message")
	messageInfo = json.loads(request.data)
	sender = messageInfo['sender']
	receiver = messageInfo['receiver']
	message = messageInfo['message']

	#TODO: if debug:
	print("  sender:",sender)
	print("  recver:",receiver)
	print("  msg:",message, flush=True) #flush=True because console doesn't show prints in realtime


	#raise Exception("send message", message)
	responseObject = {}
	responseObject['messageID'] = 'dsfdsf37129';
	responseObject['message'] = message

	if not receiver:
		#TODO: figure out correct error code. 406 https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
		#TOdO: meaningful response, e.g. tell user they need a receiver
		return responseObject, 406

	return responseObject, 200


@app.route('/getrecipients',methods=["GET"])
def get_recipients():


	responseObject = {}
	responseObject['recipients'] = [{'id':2, 'name':'Akriti'},{'id':3, 'name':'Ryan'},{'id':4, 'name':'Julie'}]
	return responseObject, 200
