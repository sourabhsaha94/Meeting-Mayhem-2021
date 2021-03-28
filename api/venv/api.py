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

    

    # the_response = Response()
    # the_response.code = "expired"
    # the_response.error_type = "expired"
    # the_response.status_code = 200
    # the_response._content = b'{ "uri" : "1234" }'

    # print(the_response.json())

    responseObject = {}
    responseObject['URI'] = '1234';
    return responseObject, 200
