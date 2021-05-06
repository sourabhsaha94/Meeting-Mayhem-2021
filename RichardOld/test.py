from datetime import datetime

timeRaw = datetime.now()
timeStr = timeRaw.strftime("%m/%d/%Y_%H:%M:%S")
print(timeStr)
#db.create_all()

print("test4")

times = []

#print ("hello world")


for i in range(24):
	if i < 12:
		timeNum = i+1
		timeHolder = str(timeNum) + "AM"
		times.append(timeHolder)
	else:
		timeNum = i-11
		timeHolder = str(timeNum) + "PM"
		times.append(timeHolder)

print(times)


messages = [{"Sender":"Alice", "Recipient":"Bob", "Time":"Default", 
					"Place":"Park", "Key":"None", "Encrypt":False, 
					"Hash":False, "Sign":False, "Message":"The quick brown fox jumped over the lazy dog"},
				{"Sender":"Alice", "Recipient":"Eve", "Time":"12PM", 
					"Place":"Default", "Key":"None", "Encrypt":False, 
					"Hash":False, "Sign":False, "Message":"Hello World!"}]