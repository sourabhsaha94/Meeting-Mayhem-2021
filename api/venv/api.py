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
    print(user)  
    print(pwd) 



    responseObject = {}
    responseObject['URI'] = '1234';
    return responseObject, 200
