import string,time,datetime,serial
from ClockAideModes import *
from ClockAideHelpers import *

BaudRate = 9600
keypadLocation = "/dev/ttyACM0"
motorLocation = "/dev/ttyACM1"

keypad = serial.Serial(keypadLocation,BaudRate)
motor = serial.Serial(motorLocation,BaudRate)

currentTime = ""
id = ""
mode = ""

# time.sleep(2)
# keypad.flush()
# motor.flush()

# mode = normal

modes =	("NORMAL",  "CHECK_ID",  "READ", "SET", "TEACHER")

stuff =	{
	'0'  : "NORMAL", \
	'1'  : "CHECK_ID", \
	'2'  : "READ",\
	'3'  : "SET", \
	'4'  : "TEACHER", \
	'5'  : "GOOD", \
	'6'  : "WRONG", \
	'7'  : "WAKE_UP",\
	'8'  : "GET_TIME", \
	'9'  : "RESET", \
	'10' : "UNKNOWN"
	}
	
command = {
	"good"		: '5', \
	"wrong"		: '6', \
	"wake_up"	: '7',\
	"get_time"	: '8',\
	"reset"		: '9',\
	"unknown"	: '10'
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

def initialization():
	global mode
	time.sleep(2)
	keypad.flush()
	motor.flush()
	
	global currentTime = datetime.datetime.now()
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
		global id = keypad.read(3)
		global name = namesID[id]		## replace this with function to check input ID vs. database
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

	hourFile = "./VoiceMap/Hours/"+str(hour)+".wav"
	if minute is "0":
		minuteFile="./VoiceMap/Wildcard/oclock.wav"
	else:
		minuteFile="./VoiceMap/Minutes/"+str(minute)+".wav"

	playVoiceMap = "mplayer %s 1>/dev/null 2>&1 " + hourFile + " " + minuteFile
	os.system(playVoiceMap)
