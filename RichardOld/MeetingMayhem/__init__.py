"""
File:    __init__.py
Author:  Richard Baldwin
Date:    11/23/2020
E-mail:  richardbaldwin@umbc.edu
Description: this is the python file that manages the package
"""
"""
#imports

each import is used to build high level parts for the application
anything that should be abel to be accessed by any other python file
within the package should be here
"""
from flask import Flask #this imports flask, used to create the flask application
from flask_sqlalchemy import SQLAlchemy #this is for managing databases
from flask_bcrypt import Bcrypt #this is for encryption things
from flask_login import LoginManager # this manages logins

#constants
PW_File = "login.txt" #this is the file name for the password file
DB_FILE_NAME = "site.db" #this is the name for the database file
# set app as flask site
app = Flask(__name__)
# secret key, this is for CSRF protection
app.config['SECRET_KEY'] = 'V^sPcWUSvLlNo5uY8bCe'
#database  setup, the DB is attached to the db variable
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+DB_FILE_NAME
db = SQLAlchemy(app)
#encryption setup
bcrypt = Bcrypt(app)
#login setup
loginManager = LoginManager(app)
loginManager.login_view = "login"
#import routes for the flask app
from MeetingMayhem import routesMM
