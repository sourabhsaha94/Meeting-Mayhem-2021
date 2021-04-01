"""
File:    routesMM.py
Author:  Richard Baldwin
Date:    10/2/2020
E-mail:  richardbaldwin@umbc.edu
Description: this manages all the routes within the flask app

each route is contained in a function, the first few are for login stuff
followed by user view stuff, then by adversary stuff. at the end is 
functions for misc. tasks      
"""
#imports
from flask import render_template, url_for, flash, redirect, request, session
#from MeetingMayhem import app
from venv import app
from venv.formsMM import userMessageForm, LoginForm, advMessageForm, menuForm
from venv.DB_MM import messageSplit, addMessageToDB, checkUserLogin, updateGMRole, userGen
from flask_login import login_user, current_user, logout_user, login_required

#data holders
allNames = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
times = ['1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', 
		'10AM', '11AM', '12AM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', 
		'7PM', '8PM', '9PM', '10PM', '11PM', '12PM']
places = ["Park", "Back-Ally", "School", "Ice-Rink", "Skate-Park", 
		"Jeff's-House", "Giant", "Behind-The-Giant", "Maker-Space", 
		"Library", "Trailhead", "Crag", "Boat-Launch", "Farm", "Harbor", 
		"Range", "Zoo", "Gym", "Parking-Lot", "Work"]
pubKeys = ["Alice-PubKey", "Bob-PubKey", "Charlie-PubKey", 
		"Dave-PubKey", "Eve-PubKey"]

#Routes
"""
each function has a set of decorators
the @app.route() is what tells flask what's allowed to happen on that page
the first argument, a string, is the path to the website, the second argument 
is the methods allowed

there is also an @login_required decorator, this is used to restrict those pages 
to deny anyone not logged in. logins are managed by flask_login

if a page has two @app.route()s, either path will take you to that page

each route has this bit of code, i'll explain it below
	
	if request.method == "GET":
		return render_template('login.html', title='Login', form = form)

this checks if the request is a get request, then renders the appropreate html file
each html file can be built from higher up ones. the highest is base.html which sets the 
layout of every page on the site more details are in login.html

the second argument in render_template is the title, this will set both the title on the tab
of the browser, and also the home button on the page if applicable

anythin after that is variables being passed into the html page, most often it's the form
(which you can find in formsMM.py). the syntax is HTMLVarName = PythonVarName. i usually
keep them the same for conviennece
"""
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
	#check if logged in
	if current_user.is_authenticated:
		return redirect(url_for('mainMenu'))
		
	form = LoginForm()
	#output website
	if request.method == "GET":
		return render_template('login.html', title='Login', form = form)
	# input forms

	#if request.method == "POST":
	if form.validate_on_submit():
		userLoginSuccess, userObject = checkUserLogin(form.username.data, form.password.data)
		if userLoginSuccess:
			login_user(userObject)
			return redirect(url_for('mainMenu'))
		else:
			return "login failed"
	#if all else fails, return back to login	
	return redirect(url_for('login'))

@app.route("/logout")
def logout():
	logout_user()
	return "logged out"

@app.route("/menu", methods=["GET", "POST"])
@login_required
def mainMenu():
	#if not GM, redirect to appropreate page
	if current_user.role1 == "User":
		return redirect(url_for('userHome'))
	elif current_user.role1 == "Spectator":
		return redirect(url_for('logout'))
	elif current_user.role1 == "Adversary":
		return redirect(url_for('advHome'))
	#check if game has already been setup

	#vars
	form = menuForm()

	#output website
	if request.method == "GET":
		return render_template('mainMenu.html', title='Menu', form = form)
	# input forms
	if request.method == "POST":
		if form.validate_on_submit():
			#put users into list
			userList = [form.user1.data, form.user2.data, form.user3.data]
			if form.user4.data:
				userList.append(form.user4.data)
			if form.user5.data:
				userList.append(form.user5.data)
			#update GM
			#if if gm is adversary, update gm secondary role to be adversary
			GMisAdversary = form.GMasAdv.data
			if GMisAdversary:
				updateGMRole("Adversary")
			#genererate users
			userGen(GMisAdversary, userList, form.numSpec.data)
			#redirect
			return redirect(url_for('advHome'))
	return redirect(url_for('mainMenu'))
	

#user stuff
@app.route("/user", methods=["GET", "POST"])
@app.route("/user/home", methods=["GET", "POST"])
@login_required
def userHome():
	userPagesCheck()
	form = userMessageForm() #important, do not touch

	username = allNames[0] #formatting
	names = allNames[1:] #formatting
	keys = ["Alice-PrivKey", "1337KeyZ-SymKey"] #formatting
	keys = pubKeys + keys #formatting

	turnComplete = False #gm controls
	messageSent = False #gm controls
	roundComplete = False #gm controls


	#Test (Trent)
	turnDisplay = "TURN IS ONE"

	#vars to be pulled from trent
	gameRound = 1

	#vars from richard
	userID = "Alice"
	#Formating-> round (integer), sender (string), recipient (string), time_choice (int), place
	#			 (string), key (string), encrypt (boolean), message (string), message ID (int), original sender (string)
	"""

	messageDict = {"Round":messageInput.round_number, "Sender":messageInput.sender, "Recipient":messageInput.recipient, "Time":messageInput.time_choice, 
				"Place":messageInput.place_choice, "Key":messageInput.key_choice, "Encrypt":messageInput.encrypt_check, "Message":messageInput.message, 
				"MessageID":messageInput.message_id, "OriginalSender":messageInput.originalSender}
	"""


	#output website
	if request.method == "GET":
		return render_template('userHome.html', title='Home', form = form, 
			names = names, username = username, times = times, places = places,
			keys = keys)
	# input forms
	if request.method == "POST":
		#variable bindings
		#sender dropdown
		sender = request.form['sender']
		#Recipient dropdown
		recipient = request.form['recipient']
		#time dropdown
		timeChoice = request.form['timeChoice']
		#place dropdown
		placeChoice = request.form['placeChoice']
		#key dropdown
		keyChoice = request.form['keyChoice']


	if form.submit and not messageSent:
		#bind all details to message dict
		messageDict = {"Round":gameRound, "Sender":sender, "Recipient":recipient, "Time":timeChoice, 
						"Place":placeChoice, "Key":keyChoice, "Encrypt":form.encryptCheck, "Message":form.message, 
						"MessageID":1, "OriginalSender":sender}
		#set message sent to true to disallow messages to be edited after they are sent
		messageSent = True
		#add message to db
		addMessageToDB(messageDict, userID)

	else:
		#return "you already sent a message" alert
		pass

	#send message if turn is complete
	if turnComplete:
		#check if message was submited
		if messageSent:
			#if true, bind message to DB, and notefy main game program

			#append message to sent Messages html
			pass
		else:
			#else forward "no message sent" to main game program
			pass

	#update UI if round is complete
	if roundComplete:
		#reset vars
		messageSent = False
		roundComplete = False
		turnComplete = False
		# append recieved messages to html
@app.route("/user/sent_messages", methods=["GET", "POST"])
@login_required
def userSentMessages():
	userPagesCheck()
	form = userReferenceBoxChoice()
	# build messages for output to website
	Round, Sender, Recipient, Time, Place, Key, Encrypt, MessageText, MessageID, OriginalSender = messageSplit(messages)
	messageNum = len(messages)

	#output website
	if request.method == "GET":
		return render_template('userSentMessages.html', title='Sent Messages', 
				form = form, Round = Round, Sender = Sender, Recipient = Recipient, 
				Time = Time, Place = Place, Key = Key, Encrypt = Encrypt, MessageText = MessageText,
				messageNum = messageNum)
	# input forms
	if request.method == "POST":
		pass
@app.route("/recieved_messages", methods=["GET", "POST"])
@login_required
def userRecievedMessages():
	userPagesCheck()
	form = userReferenceBoxChoice()
	#output website
	if request.method == "GET":
		return render_template('userRecievedMessages.html', title='Sent Messages')
	# input forms
	if request.method == "POST":
		pass

#aversary stuff 
@app.route("/adversary", methods=["GET", "POST"])
@app.route("/adversary/home", methods=["GET", "POST"])
@login_required
def advHome():
	isGM = advPagesCheck()
	#set gm view 
	if isGM:
		htmlFile = 'advGM.html'
	else:
		htmlFile = "advNonGM.html"
	form = advMessageForm()
	gmForm = "test"
	keys = pubKeys
	names = allNames



	gameState = ""
	encryptEnable = ""

	#generate list for times



	#output website
	if request.method == "GET":
		return render_template(htmlFile, title='Adversary Home', form = form, 
			names = names, times = times, places = places,
			keys = keys)
	# input forms
	if request.method == "POST":
		#variable bindings
		pass
@app.route("/adversary/messages", methods=["GET", "POST"])
@login_required
def advMessages():
	isGM = advPagesCheck()
	#vars
	form = advMessageForm()
	names = allNames
	# build messages for output to website
	Round, Sender, Recipient, Time, Place, Key, Encrypt, MessageText, MessageID, OriginalSender = messageSplit(messages)
	modRound, modSender, modRecipient, modTime, modPlace, modKey, modEncrypt, modMessageText, modMessageID, modOriginalSender = messageSplit(messagesMod)
	messageNum = len(messages)

	#output website
	if request.method == "GET":
		return render_template("advMessage.html", title='Adversary Messages', form = form,
			names = names, Round = Round, Sender = Sender, Recipient = Recipient, 
				Time = Time, Place = Place, Key = Key, Encrypt = Encrypt, MessageText = MessageText,
				messageNum = messageNum, MessageID = MessageID, modRound = modRound, modSender = modSender, 
				modRecipient = modRecipient, modTime = modTime, modPlace = modPlace, modKey = modKey, 
				modEncrypt = modEncrypt, modMessageText = modMessageText, modMessageID = modMessageID, 
				OriginalSender = OriginalSender, modOriginalSender = modOriginalSender)
	# input forms
	if request.method == "POST":
		#variable bindings
		pass

#misc
def userPagesCheck():
	#if not user, redirect to appropreate page
	if current_user.role1 == "Adversary":
		return redirect(url_for('advHome'))
	elif current_user.role1 == "Spectator":
		return redirect(url_for('logout'))
	elif current_user.role1 == "GM":
		if current_user.role2 == "Adversary":
			return redirect(url_for('advHome'))
		elif current_user.role2 == "Spectator":
			return redirect(url_for('logout'))
def advPagesCheck():
	#if not adversary, redirect to appropreate page and set isGM for gm  controls
	isGM = False
	if current_user.role1 == "User":
		return redirect(url_for('userHome'))
	elif current_user.role1 == "Spectator":
		return redirect(url_for('logout'))
	elif current_user.role1 == "GM":
		if current_user.role2 == "Adversary":
			isGM = True
		elif current_user.role2 == "Spectator":
			return redirect(url_for('logout'))
	return(isGM)
