
"""
File:    DB_MM.py
Author:  Julia Nau, Richard Baldwin
Date:    5/1/2021
E-mail: jnau1@umbc.edu
		richardbaldwin@umbc.edu
Description: this manages DB thigs and password things

"""
#from MeetingMayhem import db, DB_FILE_NAME, PW_File, loginManager, bcrypt
from venv import db, DB_FILE_NAME, PW_File, loginManager, bcrypt
from flask_login import UserMixin
import subprocess
from datetime import datetime
import secrets
import string

#TODO: Remove this, it's only for testing one error.
from flask_sqlalchemy import SQLAlchemy #this is for managing databases
from sqlalchemy import exc, func

#constants
#all letters and numbers for random PW generation
CHARLIST = string.ascii_letters + string.digits
#global vars
#TODO: dynamically update messageIDCount based on the database's state
messageIDCount = 0 #this isitterated as time goes on, might move
messageIDList = [] #this holds all message id's for checking
#this is the location for the flask app, can be automated later
workingFolder = "/" #TODO: Figure this out


#need for login, loads user
@loginManager.user_loader
def load_user(user_id):
	return Userdata.query.get(int(user_id))
"""
#DB thigs

each database object is a class the db.Model is needed for this
UserMixin is used to manage some functionality for login stuff
"""
#user data such as login stuff
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True) #this is the id for the DB entry
	email = db.Column(db.String)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	#this binds the user to their messages
	#sent_messages = db.relationship('UserSentMessages', backref = "username", lazy=True)
'''
#user messages
class UserSentMessages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.String(20), nullable=False)
	recipient = db.Column(db.String(20), nullable=False)
	time_choice = db.Column(db.String(4), nullable=False)
	place_choice = db.Column(db.String(20), nullable=False)
	key_choice = db.Column(db.String(20), nullable=False)
	message = db.Column(db.String(40), nullable=False)
	encrypt_check = db.Column(db.Boolean, nullable=False)
	message_id =  db.Column(db.Integer, unique=True, nullable=False)
	#this is from
	user_id = db.Column(db.Integer, db.ForeignKey('userdata.id'), nullable=False)
	#this is the same as sender unless modefied by the adversary
	originalSender = db.Column(db.String(20), nullable=False)
	round_number = db.Column(db.Integer, nullable=False)

def sendMessage(sender,receiver,text):

	print("sendMessage sender", sender, sender[0], flush=True)
	#TODO: unify receiver vs recipient vs... destination?
	messageDict = {"Round":-1, "Sender":sender[0]['name'], "Recipient":receiver,
	"Time":1,  "Place":1, "Key":1,
	"Encrypt":False, "Message":text,  "MessageID":1,
	"OriginalSender":sender}

	userID = sender[0]['id'] #TODO: this could eventually be adversary?

	addMessageToDB(messageDict, userID)


#functions
#add messages to db
def addMessageToDB(submitedMessage, userID, messageIsModded = False, oMessage = {}):
	global messageIDCount
	#if messageIsModded, add to appropreate DB
	# update ID
	if messageIsModded:
		#ready data for db input
		messageID=oMessage["MessageID"]
		originalSender = oMessage["Sender"]
	else:
		#increment message count
		messageIDCount += 1
		messageID = messageIDCount
		#if message count is not unique, increment until it is
		while messageID in messageIDList:
			messageID += 1
		#add new id to list
		#messageIDList.add(messageID)
		messageIDList.append(messageID)
		#ready data for db input
		originalSender = submitedMessage["Sender"]

		print("addMessage submittedMessage",submitedMessage,flush=True)
	#ready data for db input
	message = UserSentMessages(sender=submitedMessage["Sender"], recipient=submitedMessage["Recipient"], time_choice=submitedMessage["Time"],
		place_choice=submitedMessage["Place"], key_choice=submitedMessage["Key"], message=submitedMessage["Message"],
		encrypt_check=submitedMessage["Encrypt"], message_id=messageID, originalSender = originalSender, round_number=submitedMessage["Round"],
		user_id = userID)
	#submit db
	db.session.add(message)
	#commit db
	db.session.commit()

#pull messages from db
def getUserMessageFromDB(usernameInput, gameRound = -1):
	#get all messages from UserSentMessages where recipient is our user
	messageList = UserSentMessages.query.filter_by(recipient=usernameInput).all()

	print("getUserMessageFromDB",messageList,flush=True)
	formattedMessageList = []
	#TODO: format game round in the SQL query instead?
	if gameRound == -1:
		#if no gameround chosen, return all messages
		for message in messageList:
			formattedMessageList.append(formatMessagesFromDB(message))
	else:
		#else only add messages in round
		for message in messageList:
			if message.round_number == gameround:
				formattedMessageList.append(formatMessagesFromDB(message))
	return(formattedMessageList)
# takes message from db, and outputs it as dict
def formatMessagesFromDB(messageInput):
	messageDict = {"Round":messageInput.round_number, "Sender":messageInput.sender, "Recipient":messageInput.recipient, "Time":messageInput.time_choice,
				"Place":messageInput.place_choice, "Key":messageInput.key_choice, "Encrypt":messageInput.encrypt_check, "Message":messageInput.message,
				"MessageID":messageInput.message_id, "OriginalSender":messageInput.originalSender}

	#Formating-> round (integer), sender (string), recipient (string), time_choice (int), place
	#			 (string), key (string), encrypt (boolean), message (string), message ID (int), original sender (string)
	return(messageDict)

# return false if any part of message is different
def messageCompare(message1, message2):
	if message1["Round"] != message2["Round"]:
		return(False)
	elif message1["Sender"] != message2["Sender"]:
		return(False)
	elif message1["Recipient"] != message2["Recipient"]:
		return(False)
	elif message1["Time"] != message2["Time"]:
		return(False)
	elif message1["Place"] != message2["Place"]:
		return(False)
	elif message1["Key"] != message2["Key"]:
		return(False)
	elif message1["Encrypt"] != message2["Encrypt"]:
		return(False)
	elif message1["Message"] != message2["Message"]:
		return(False)
	elif message1["MessageID"] != message2["MessageID"]:
		return(False)
	elif message1["OriginalSender"] != message2["OriginalSender"]:
		return(False)
	else:
		return(True)

#generate password using charlist
def messageSplit(messages):
	# this takes a list of message dicts and splits them into individual lists
	# each list contains 1 part of the dict in the order they occor
	# the message can be re built by going through each list with
	# a single value as the key
	Round = []
	Sender = []
	Recipient = []
	Time = []
	Place = []
	Key = []
	Encrypt = []
	MessageText = []
	MessageID = []
	OriginalSender = []
	for message in messages:
		Round.append(message["Round"])
		Sender.append(message["Sender"])
		Recipient.append(message["Recipient"])
		Time.append(message["Time"])
		Place.append(message["Place"])
		Key.append(message["Key"])
		Encrypt.append(message["Encrypt"])
		MessageText.append(message["Message"])
		MessageID.append(message["MessageID"])
		OriginalSender.append(message["OriginalSender"])

	return(Round, Sender, Recipient, Time, Place, Key, Encrypt, MessageText, MessageID, OriginalSender)
#adds user to db
def addUserDB(usernameInput, passwordInput, role1Input, role2Input = "", autoRollback = True):

	try:
		user = Userdata(username = usernameInput, password = passwordInput, role1 = role1Input, role2 = role2Input)
		#submit db
		db.session.add(user)
		#commit db
		db.session.commit()
	except exc.IntegrityError:
		if autoRollback:
			db.session.rollback()

#updates gm role after setup
def updateGMRole(newRole):
	gm = Userdata.query.filter_by(username="GM").first()
	gm.role2 = newRole
#setup db
def dbInit():
	print("dbInit() starting",flush=True)

	#TODO: consider if necessary.
	#check if paused file exists, set pause if true
	with open("pause.txt", "r") as pauseFile:
		pausedRaw = pauseFile.read()
		if pausedRaw == "True":
			paused = True
		elif pausedRaw == "False":
			paused = False
	if paused:
		#if paused, mark paused file as false. i.e. unpause
		print("Am paused!",flush=True)
		with open("pause.txt", "w") as pauseFile:
			pauseFile.write("False")
	else:
		#else backup and delete old db, and create new DB.
		#get time info
		timeStr = getTime()
		#backup and delete db
		backupNDeleteDB(timeStr)
		#create new db
		db.create_all()

		#move pwfile to match backup db, delet pw file
		backupFileName = timeStr + "--" + PW_File + ".bak"
		copy(PW_File, backupFileName)
		deleteFile(PW_File)

		#generate GM
		encryptedPassword = initGMSetup()

		try:
			addUserDB("GM", encryptedPassword, "GM", "Spectator")
		except: #TODO: You can do this but you shouldn't
			print("Whoops! We've already added GM!",flush=True)
			db.session.rollback() #fail gracefully, reset the cursor to prior state to "clear" the bad addition.
			#return False
		#print("passed the add GM line",flush=True)

		#make messageIDCount reflect the next message ID to be given
		#check database for existing messages, get max.
		global messageIDCount
		messageIDCount = db.session.query(func.max(UserSentMessages.message_id)).scalar()

		print("  max ID",messageIDCount,flush=True)
		#print("past max ID",flush=True)


		with open("loginDefault.txt", "r") as loginFile:
			lines = list(loginFile)
			print("Lines:")
			print(lines,flush=True)
			for line in lines:
				a = line.split(":")
				if a[0] == "GM":
					continue
				#TODO: remove/integrate userGen()
				#print("making user",a[0],flush=True)
				CreateUser("User",a[0],a[1]) #pwLen is defaulted #

		print("passed the login Default line",flush=True)

		#TODO: Figure out why dbInit gets called more than once sometimes
		#Apparently that's "because of the Reloader"
		#TODO: remove this very risky, confusing workaround
		#dbInit.code = (lambda:None).code
#close db
def dbExit(pause = False):
	if pause:
		#if paused, mark paused file as true, and do not delete db or password file
		with open("pause.txt", "w") as pauseFile:
			pauseFile.write("True")
	else:
		#else backup and delete db file, delete password file
		#get time info
		timeStr = getTime()
		#backup and delete db
		backupNDeleteDB(timeStr)
		#delet pw file
		deleteFile(PW_File)
#backup db
def backupNDeleteDB(timeStr):
		#format backup file name
		backupFileName = timeStr + "--" + DB_FILE_NAME + ".bak"
		#copy backup file
		copy(DB_FILE_NAME, backupFileName)
		#delete db file
		deleteFile(DB_FILE_NAME)
#Get time formatted
def getTime():
	timeRaw = datetime.now()
	timeStr = timeRaw.strftime("%m/%d/%Y_%H:%M:%S")
	return(timeStr)
#checks if user can login
def checkUserLogin(usernameInput, passwordInput):
	print("checkUserLogin:", usernameInput, passwordInput, flush=True)
	userToCheck = Userdata.query.filter_by(username=usernameInput).first()

	print("checkUserLogin query:", userToCheck,flush=True)

	passCheckResult = passwordCheck(userToCheck.password, passwordInput)
	if userToCheck and passCheckResult:
		return(True, userToCheck)
	else:
		#TODO: it is insecure to tell the user if it's username wrong or password wrong
		if not userToCheck:
			print("user not found?",flush=True)
		if not passCheckResult:
			print("Wrong password!",flush=True)
		return(False, userToCheck)
#copy files
def copy(src, dst):
	src = workingFolder + src
	dst = workingFolder + dst
	subprocess.call(["cp", str(src), str(dst)])
#delete files
def deleteFile(fileName):
	fileName = workingFolder + fileName
	subprocess.call(["rm", str(fileName)])
#generate users
def userGen(GMisAdversary = True, users = ["Alice", "Bob", "Charlie", "Dan", "Eve"], numSpectator = 1, pwLen = 12):
	#update GM
	#if if gm is not adversary, create network user, and decrement spectators
	if not GMisAdversary:
		numSpectator -= 1
		CreateUser("Adversary", "Adversary", pwLen)

	#generate spectators
	for i in range(numSpectator):
		SpectatorName = "Spectator" + str(i+1)
		CreateUser("Spectator", SpectatorName, pwLen)


	#generate users
	for username in users:
		CreateUser("User", username, pwLen)


#creates user w/ random password (can be found in login.txt)
def CreateUser(role, name, pwLen = 12):
	#generate username and password for GM
	#TODO: Revert/update this to make actually secure passwords
	#password = PasswordGen(pwLen)
	password = "password"

	#output info to file
	with open(PW_File, "a") as loginInfoFile:
		info = name + ":" + password + "\n"
		loginInfoFile.write(info)

	#encrypt password
	encryptedPassword = passwordHashGen(password)
	#add user to db
	addUserDB(name, encryptedPassword, role)

#functions from pwgen
#generate password using charlist
def PasswordGen(pwLen = 12):
	password = ''.join(secrets.choice(CHARLIST) for i in range(pwLen))
	return password
def passwordHashGen(password):
	return(bcrypt.generate_password_hash(password).decode("utf-8"))
#initial gm setup
def initGMSetup(pwLen = 12):
	#generate username and password for GM
	password = PasswordGen(pwLen)
	#output info to file
	with open(PW_File, "a") as loginInfoFile:
		info = "GM:" + password + "\n"
		loginInfoFile.write(info)

	#encrypt password
	encryptedPassword = bcrypt.generate_password_hash(password).decode("utf-8")
	return(encryptedPassword)
	#add gm to db from MeetingMayhem.DB_MM import addUserDB, updateGMRole
#check password for login
def passwordCheck(hashToCompare, passwordToCheck):
	#TODO: password for Alice is 'a', password given is 'a', but they don't match.
	print("passwordCheck",hashToCompare,passwordToCheck,passwordHashGen(passwordToCheck),flush=True)
	return(bcrypt.check_password_hash(hashToCompare, passwordToCheck))
'''