import time
import json
from flask import Flask
from flask import render_template, url_for, flash, redirect, request, session
from requests.models import Response
from venv import DB_MM
from venv import app

#Removed for causing problems. Is already in __init__.py
#app = Flask(__name__)
#added a commit
@app.route('/time')
def get_current_time():
	return {'time': time.time()}

@app.route('/login',methods=["POST"])
def login():
	print("inside login")
	loginInfo = json.loads(request.data)
	user = loginInfo['email']
	pwd = loginInfo['password']

	loginExists = True
	loginExists = DB_MM.checkUserLogin(user, pwd)
	print("  testing login:",loginExists)


	responseObject = {}
	responseObject['URI'] = '1234';

	print("",flush=True)
	retcode = 200
	if not loginExists[0]:
		retcode = 406 #TODO: right code

	retcode = 200 #Force it to work regardless of if password is bad.
	#TODO: checkUserLogin is doing a different hash for writing the password vs checking the password

	if loginExists[1] is None:
		print("get_current says wrong username",user,flush=True)
		retcode = 407

	return responseObject, retcode

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

	#TODO: unify sendMessage and send_message
	DB_MM.sendMessage(sender,receiver,message)

	print("  post sendMessage",flush=True)
	#raise Exception("send message", message)
	responseObject = {}
	responseObject['messageID'] = 'dsfdsf37129';
	responseObject['message'] = message

	if not receiver:
		#TODO: figure out correct error code. 406 https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
		#TOdO: meaningful response, e.g. tell user they need a receiver
		return responseObject, 406

	return responseObject, 200

@app.route('/getmessages',methods=["POST"])
def get_messages():
	username = request.args.get('user', default = 'Alice', type = str)
	print("inside get message")
	print(username)
	#messageInfo = json.loads(request.data)
	#sender = messageInfo['sender']
	#receiver = messageInfo['receiver']
	#message = messageInfo['message']

	print("  so:",username,flush=True)

	#msgs = DB_MM.getUserMessageFromDB(username)

	#print("  msgs:", msgs, flush=True)

	responseObject = {}
	msgs = [{
        'sender': "Sudha",
        'message': "Hi Akriti let's meet in the Library at 4 pm"
    }, {
      'sender': "Ryan",
      'message': "Hey There!"
    }]
	responseObject['messages'] = msgs
	
	return responseObject, 200

@app.route('/getrecipients',methods=["GET"])
def get_recipients():

	responseObject = {}
	responseObject['recipients'] = [{'id':2, 'name':'Akriti'},{'id':3, 'name':'Ryan'},{'id':4, 'name':'Julie'}]
	return responseObject, 200
