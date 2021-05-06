
"""
File:    Login_MM.py
Author:  Julia Nau, Richard Baldwin
Date:    5/5/2021
E-mail: jnau1@umbc.edu
		richardbaldwin@umbc.edu
Description: this file manages login. it is to be called my Routes_MM.py
			It interfaces with DB_PW_MM.py

"""

"""
this class manages Login
functions include
	LoginUser
	LogoutUser
	CreateAccount
"""
def MM_LoginUser(passwordInput, emailInput):
	"""
	this function accepts a password, and email strings
	it returns true if succesfully logged in, and false
	if login failure
	"""
	#attempt to login
	#if succesfull, return true, else false
	userToCheck = Userdata.query.filter_by(email=emailInput).first()
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
	pass
def MM_LogoutUser():
	pass
def MM_CreateAccount():
	pass

#copied functions
def CreateUser(role, name, pwLen = 12):

	#creates user w/ random password (can be found in login.txt)
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

#Get time formatted
def getTime():
	timeRaw = datetime.now()
	timeStr = timeRaw.strftime("%m/%d/%Y_%H:%M:%S")
	return(timeStr)

#need for login, loads user
@loginManager.user_loader
def load_user(user_id):
	return Userdata.query.get(int(user_id))