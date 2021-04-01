
"""
File:    DB_MM.py
Author:  Richard Baldwin
Date:    10/2/2020
E-mail:  richardbaldwin@umbc.edu
Description: this manages DB thigs and password things

"""
#from MeetingMayhem import db, DB_FILE_NAME, PW_File, loginManager, bcrypt
from venv import db, DB_FILE_NAME, PW_File, loginManager, bcrypt
from flask_login import UserMixin
import subprocess
from datetime import datetime
import secrets
import string


#constants
#all letters and numbers for random PW generation
CHARLIST = string.ascii_letters + string.digits
#global vars
messageIDCount = 0 #this isitterated as time goes on, might move
messageIDList = [] #this holds all message id's for checking
#this is the location for the flask app, can be automated later
workingFolder = "/home/eyeclept/Documents/FlaskGame/test/MeetingMayhem/"

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
class Userdata(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True) #this is the id for the DB entry
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	role1 = db.Column(db.String(20), nullable=False) #this is the users role
	role2 = db.Column(db.String(20)) #if the user is GM, the second role tells their main role
	#this binds the user to their messages
	sent_messages = db.relationship('UserSentMessages', backref = "username", lazy=True)

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

#functions
#add messages to db
def addMessageToDB(submitedMessage, userID, messageIsModded = False, oMessage = {}):
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
		messageIDList.add(messageID)
		#ready data for db input
		originalSender = submitedMessage["Sender"]
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
	#get user from username
	user = Userdata.query.filter_by(username=usernameInput).first()
	#get users messages
	messageList = user.UserSentMessages
	formattedMessageList = []
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
def addUserDB(usernameInput, passwordInput, role1Input, role2Input = ""):
	user = Userdata(username = usernameInput, password = passwordInput, role1 = role1Input, role2 = role2Input)
	#submit db
	db.session.add(user)
	#commit db
	db.session.commit()
#updates gm role after setup
def updateGMRole(newRole):
	gm = Userdata.query.filter_by(username="GM").first()
	gm.role2 = newRole
#setup db
def dbInit():
	print("dbInit() starting",flush=True)
	#check if paused file exists, set pause if true
	with open("pause.txt", "r") as pauseFile:
		pausedRaw = pauseFile.read()
		if pausedRaw == "True":
			paused = True
		elif pausedRaw == "False":
			paused = False
	if paused:
		#if paused, mark paused file as false. i.e. unpause
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
		backupFlieName = timeStr + "--" + PW_File + ".bak"
		copy(PW_File, backupFlieName)
		deleteFile(PW_File)

		#generate GM
		encryptedPassword = initGMSetup()
		addUserDB("GM", encryptedPassword, "GM", "Spectator")
		print("GM user added")
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
		backupFlieName = timeStr + "--" + DB_FILE_NAME + ".bak"
		#copy backup file
		copy(DB_FILE_NAME, backupFlieName)
		#delete db file
		deleteFile(DB_FILE_NAME)
#Get time formatted
def getTime():
	timeRaw = datetime.now()
	timeStr = timeRaw.strftime("%m/%d/%Y_%H:%M:%S")
	return(timeStr)
#checks if user can login
def checkUserLogin(usernameInput, passwordInput):
	userToCheck = Userdata.query.filter_by(username=usernameInput).first()
	if userToCheck and passwordCheck(userToCheck.password, passwordInput):
		return(True, userToCheck)
	else:
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
	return(bcrypt.check_password_hash(hashToCompare, passwordToCheck))
