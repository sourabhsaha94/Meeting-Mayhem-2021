import time
import json
from flask import Flask
from flask import render_template, url_for, flash, redirect, request, session
from requests.models import Response

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


    responseObject = {}
    responseObject['URI'] = '1234';
    return responseObject, 200

@app.route('/sendmessage',methods=["POST"])
def send_message():
    print("inside send message")
    messageInfo = json.loads(request.data)
    sender = messageInfo['sender']
    receiver = messageInfo['receiver']
    message = messageInfo['message']


    responseObject = {}
    responseObject['messageID'] = 'dsfdsf37129';
    return responseObject, 200


@app.route('/getrecipients',methods=["GET"])
def get_recipients():


    responseObject = {}
    responseObject['recipients'] = [{'id':2, 'name':'Akriti'},{'id':3, 'name':'Ryan'},{'id':4, 'name':'Julie'}]
    return responseObject, 200
