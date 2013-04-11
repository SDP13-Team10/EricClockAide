from ClockAideHelpers import *

def initialization():
	time.sleep(2)
	keypad.flush()
	motor.flush()
	
	currentTime = datetime.datetime.now()
	print(keypad.write(currentTime.strftime("%H, %M, %S, %d, %m, %Y")))
	print(motor.write(currentTime.strftime("%H, %M, %S, %d, %m, %Y")))
	
	time.sleep(2)
	
	mode = modes[0]
	
def normal():
	try:
		comm = stuff[str(keypad.read())]		## use different method other than stuff dictionary
		
		speakTime(nowHour(), nowMinute())
		if comm == "WAKE_UP":					## send check ID signal to keypad and motor
			print(keypad.write(modeLookUp["check_id"]))
			print(motor.write(modeLookUp["check_id"]))
			
			return modes[1]						## return statements???

	except KeyError:
		print "Error!!!"						## put some logging functionality
		
		return modes[0]

def checkID():
	try:
		id = keypad.read(3)
		name = namesID[id]		## replace this with function to check input ID vs. database
		if name:
			print(keypad.write('5'))			## Sends "Correct" Code to Keypad
			time.sleep(2)
			print(keypad.write(name))			## Sends Student Name to Keypad
			
			# begging logging information
			
		return modes[int(keypad.read())]		## return statements???
		
	except KeyError:	
		print(keypad.write('6'))				## put some logging functionality
		return modes[1]							## return statements???
		
def read():
	print(keypad.write(modeLookUp["read"]))
	print(motor.write(modeLookUp["read"]))
	time.sleep(2)
	
	print(motor.write(readModeTime(id)))		## send time to be displayed to motor
	
	readTime = keypad.read(5)					## include some timeout logic

# Check time entered for correctness and send appropriate signal.
# Create a readtime function

	if checkReadTime(readTime):
		print(keypad.write(command["good"]))
		time.sleep(2)
		print(keypad.write(modeLookUp["normal"]))
		print(motor.write(modeLookUp["normal"]))
		return modes[0]
	else:
		print(keypad.write(command["wrong"]))
		time.sleep(2)
		print(keypad.write(modeLookUp["read"]))
		return modes[2]

def set():
	print(keypad.write(modeLookUp["set"]))
	print(motor.write(modeLookUp["set"]))
	time.sleep(2)
	#tme = currentTime.strftime("%H, %M")
	senttime = setModeTime(ID)
	print(keypad.write(senttime))
	
	motortime = getTimeFromMotor()
	
	if senttime == motortime:
		print(keypad.write(command["good"]))
		time.sleep(2)
		print(keypad.write(modeLookUp["normal"]))
		print(motor.write(modeLookUp["set"]))
		return modes[0]
		
	else:
		print(keypad.write(command["wrong"]))
		time.sleep(2)
		print(keypad.write(modeLookUp["set"]))
		print(motor.write(modeLookUp["set"]))
		return modes[2]
		
	time.sleep(60)
	print(keypad.write('0'))
	
