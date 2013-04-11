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
