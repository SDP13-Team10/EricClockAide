import string,time,datetime,serial,re, os
#from ClockAideModes import *
#from ClockAideHelpers import *

BaudRate = 9600
keypadLocation = "/dev/ttyUSB0"
motorLocation = "/dev/ttyACM0"

keypad = serial.Serial(keypadLocation,BaudRate)
motor = serial.Serial(motorLocation,BaudRate)

currentTime = ""
id = ""
mode = ""
comm = ""

modes =	("NORMAL",  "CHECK_ID",  "READ", "SET", "TEACHER")

stuff =	{
	'00'  : "NORMAL", \
	'01'  : "CHECK_ID", \
	'02'  : "READ",\
	'03'  : "SET", \
	'04'  : "TEACHER", \
	'05'  : "GOOD", \
	'06'  : "WRONG", \

	'07'  : "WAKE_UP",\
	'08'  : "GET_TIME", \
	'09'  : "RESET", \
	'10' : "SPEAK_TIME"
	}
MODES =	{
	'0'  : "NORMAL", \
	'1'  : "CHECK_ID", \
	'2'  : "READ",\
	'3'  : "SET", \
	'4'  : "TEACHER"
	}

COMMAND = {
	'0'  : "GOOD", \
	'1'  : "WRONG", \
	'2'  : "WAKE_UP",\
	'3'  : "GET_TIME", \
	'4'  : "RESET", \
	'5'  : "SPEAK_TIME"
	}
	
command = {
	"good"		: '0', \
	"wrong"		: '1', \
	"wake_up"	: '2',\
	"get_time"	: '3',\
	"reset"		: '4',\
	"speak_time"	: '5'
}

modeLookUp = {
	"normal"	: '0',\
	"check_id"	: '1',\
	"read"		: '2',\
	"set"		: '3',\
	"teacher"	: '4'
	}

namesID = {
	"123"  : "Eric", \
	"456"  : "Sachin", \
	"789"  : "Anita",\
	"321"  : "Joel", \
	"654"  : "Prof Leonard", \
	"987"  : "Prof Soules"
	}

def initialization():
	global mode
	global currentTime
	time.sleep(2)
	#keypad.flush()
	#motor.flush()
	
	currentTime = datetime.datetime.now()
	print(keypad.write(currentTime.strftime("%H, %M, %S, %d, %m, %Y")))
	print(motor.write(currentTime.strftime("%H, %M, %S, %d, %m, %Y")))
	
	time.sleep(2)
	
	mode = modes[0]
	
def normal():
	global comm
	print "in normal"
	try:
		print keypad.inWaiting()
		comm = COMMAND[str(keypad.read())]		## use different method other than stuff dictionary
		print "recieved" 
		print comm
		if comm == "SPEAK_TIME":
			speakTime(nowHour(), nowMinute())
			print(keypad.write(modeLookUp["normal"]))
			keypad.flushInput()
			comm = ""
			print comm
			return modes[0]
		elif comm == "WAKE_UP":					## send check ID signal to keypad and motor
			print(keypad.write(modeLookUp["check_id"]))
			print(motor.write(modeLookUp["check_id"]))
			
			return modes[1]						## return statements???

	except KeyError:
		print "Error!!!"						## put some logging functionality
		
		return modes[0]

def checkID():
	
	global id
	global name
	try:
		id = keypad.read(3)
		name = namesID[id]		## replace this with function to check input ID vs. database
		if name:
			print(keypad.write(command["good"]))			## Sends "Correct" Code to Keypad
			time.sleep(2)
			print(keypad.write(name))			## Sends Student Name to Keypad
			
			# beginning logging information
			
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
	senttime = setModeTime(id)
	print(keypad.write(senttime))

	try:

		comm = COMMAND[str(keypad.read())]
	
		if comm == "GET_TIME":
			motortime = getTimeFromMotor()
	
		#else
		
		if senttime == motortime:
			print(keypad.write(command["good"]))
			time.sleep(2)
			print(keypad.write(modeLookUp["normal"]))
			print(motor.write(modeLookUp["normal"]))
			return modes[0]
			
		else:
			print(keypad.write(command["wrong"]))
			time.sleep(2)
			print(keypad.write(modeLookUp["set"]))
			print(motor.write(modeLookUp["set"]))
			return modes[3]

	except KeyError:
		print "Error!!!"
		return modes[0]

def getTimeFromMotor():
	return "4, 15"
		
def checkReadTime(readTime):

	# compare entered time with time given to student
	# return TRUE or False
	
	# if readTime == sentTime
		# return True
		
	# else 
		# return False
	
	return True
	
def readModeTime(ID):
	
	# Get difficulty level that the student is on
	# return time based on that level
	
	return ("4, 15")
	
def setModeTime(ID):

	# Get difficulty level that the student is on
	# return time based on that level
	
	return ("4, 15")
		
def nowHour():
	return datetime.datetime.now().strftime("%I")
	
def nowMinute():
	return datetime.datetime.now().strftime("%M")
	
def speakTime(hour,minute):

	hour = str(hour)
	minute = str(minute)

	if minute is not "0":
		minute = re.sub("^0+","",minute)

	hour = re.sub("^0+","",hour)

	hourFile = "~/VoiceMap/Hours/"+str(hour)+".wav"
	if minute is "0":
		minuteFile="~/VoiceMap/Wildcard/oclock.wav"
	else:
		minuteFile="~/VoiceMap/Minutes/"+str(minute)+".wav"

	playVoiceMap = "mplayer %s 1>/dev/null 2>&1 " + hourFile + " " + minuteFile
	os.system(playVoiceMap)
def main():
	
	global mode	
	initialization()

	while 1:
		if mode == "NORMAL":
			mode = normal()
		
		elif mode == "CHECK_ID":
			mode = checkID()
			
		elif mode == "READ":
			mode = read()
		
		elif mode == "SET":
			mode = set()
		
		elif mode == "TEACHER":
			mode = teacher()

main()
