 
"""
File:    formsMM.py
Author:  Richard Baldwin
Date:    11/8/2020
E-mail:  richardbaldwin@umbc.edu
Description: this launches the Pal Game App
      
"""
#imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

#constants
MAX_SPECTATORS = 8
#forms
#user forms
class userMessageForm(FlaskForm):
	#vars
	messageContent = StringField('messageContent',
			validators=[DataRequired(), Length(min=1, max=40)])
	encryptCheck = BooleanField('encryptCheck')

#login form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=1, max=20)])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")

# main Menu form

class menuForm(FlaskForm):
	GMasAdv = BooleanField('GM is adversary')
	user1 = StringField("User1", validators=[DataRequired(), Length(min=1, max=20)])
	user2 = StringField("User2", validators=[DataRequired(), Length(min=1, max=20)])
	user3 = StringField("User3", validators=[DataRequired(), Length(min=1, max=20)])
	user4 = StringField("User4", validators=[Length(min=0, max=20)])
	user5 = StringField("User5", validators=[Length(min=0, max=20)])
	numSpec = IntegerField("Number of Spectators", validators=[DataRequired(), NumberRange(min=1, max=MAX_SPECTATORS)])
	submit = SubmitField("Finish Setup")

#adversary forms
class advMessageForm(FlaskForm):
	#vars
	messageContent = StringField('messageContent',
			validators=[DataRequired(), Length(min=2, max=40)])
	encryptCheck = BooleanField('encryptCheck')
