
"""
File:    DB_PW_MM.py
Author:  Julia Nau, Richard Baldwin
Date:    5/1/2021
E-mail: jnau1@umbc.edu
		richardbaldwin@umbc.edu
Description: this manages DB thigs and password things

"""
#from MeetingMayhem import db, DB_FILE_NAME, PW_File, loginManager, bcrypt
from venv import PW_File, loginManager, bcrypt
import secrets
import string
""" To Do:
integrate password strength checker via online something or other
"""

#constants
#all letters and numbers for random PW generation
CHARLIST = string.ascii_letters + string.digits
#functions
def PasswordGen(pwLen = 12):
	#this function generates passwords of a given length useing CHARLIST
	password = ''.join(secrets.choice(CHARLIST) for i in range(pwLen))
	return password
def passwordHashGen(password):
	#this function hashes the password using bcrypt
	return(bcrypt.generate_password_hash(password).decode("utf-8"))
def passwordCheck(DBHash, GivenHash):
	#this checks the password returning a bool. both inputs must be hashes
	#the first input is from the DB, and the second is from the form
	#be sure to use passwordHashGen on the raw password from the form
	return(bcrypt.check_password_hash(DBHash, GivenHash))