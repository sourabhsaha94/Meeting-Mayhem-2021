 
"""
File:    MeetingMayhem.py
Author:  Richard Baldwin
Date:    11/23/2020
E-mail:  richardbaldwin@umbc.edu
Description: this launches the Pal Game App
	the pal game called meeting mayhem is built within a package
	this is just some setup as well as the main function

	when MeetingMayhem is imported, that is grabbing from th __init__.py file
	it is what connects each of the other files togeather

	required software to install are below
	pip3 install Flask
	pip3 install Flask-SQLAlchemy
	pip3 install flask-bcrytp
	pip3 install flask-bcrypt
	pip3 install flask-wtf
	pip3 install flask flask-login
	pip3 install flask-login

      
"""
#import flask app
from MeetingMayhem import app

#main function
if __name__ == "__main__":
	#run in debug mode
	debugApp = True
	#launch flask app
	app.run(debug=debugApp)
	
