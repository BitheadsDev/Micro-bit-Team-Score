from microbit import*
import os

maxTeams = 5
stageWait = 3000
totalTeams = 0
activeTeam = 0

stage = 'start'
funcStage = 'start'
isFiles = False
timeCompare = 0
pressed = False
scoreFileName = 'scoreTeam'

#TEAM VARS

scores = [0,0,0,0,0]

#LED display X,Y coords
teamsXY = ((0,0), (1,0), (2,0), (3,0), (4,0))

tensXY = ((0,1), (1,1), (2,1), (3,1), (4,1), (0,2), (1,2), (2,2), (3,2), (4,2))

onesXY = ((0,3), (1,3), (2,3), (3,3), (4,3), (0,4), (1,4), (2,4), (3,4), (4,4))

#UTILITY FUNCTIONS

def fileExists(fileName):
	#Loop through all files in directory and return True if file name exists
	files = os.listdir()
	for f in files:
		if f == fileName:
			return True
	return False

def readFileInt(fileName):
	#Return the contents of the file
	with open(fileName) as h:
		a = h.read()
		return int(a)

def ifStageWait(timeCompare):
	#Return true if 3000ms have passed. Can adjust stageWait variable to lessen or lengthen wait period.
	# Have to pass timeCompare as a parameter rather than global var as timeCompare is held within memory once the function is called once.
	global stageWait
	if running_time() - timeCompare >= stageWait:
		return True
	else:
		return False

#APP STAGE FUNCTIONS
#Check if the score files exist.
# If they do load them into the list and skip to scoring.
# If they don't then go to setTeams
def checkFiles():
	global totalTeams
	global isFiles
	global stage
	global maxTeams
	global scores
	global scoreFileName
	for i in range(maxTeams):
		fileIndex = i + 1
		fileName = scoreFileName + str(fileIndex) + '.txt'
		if fileExists(fileName):
			fileContents = readFileInt(fileName)
			scores[i] = fileContents
			isFiles = True

			#For every file that exists increase the total teams by 1
			totalTeams += 1
		else:
			#get out of file checking loop if that file doesn't exist as no point in checking any further
			break
	#if no files go to setTeams
	if isFiles == False:
		stage = 'setTeams'
	else:
		stage = 'scoring'

#Ask how many teams need to be scored
def setTeams():
	global maxTeams
	global pressed
	global totalTeams
	global stage
	global stageWait
	global timeCompare
	#Increase by one if B pressed
	if button_b.was_pressed():
		timeCompare = running_time()
		pressed = True
		display.clear()
		if totalTeams < maxTeams:
			totalTeams += 1
		else:
			totalTeams = 1
		display.show(str(totalTeams))
	#Decrease by one if A pressed
	elif button_a.was_pressed():
		timeCompare = running_time()
		pressed = True
		display.clear()
		if totalTeams > 1:
			totalTeams -= 1
		else:
			totalTeams = maxTeams
		display.show(str(totalTeams))
	#If nothing pressed display '#?' i.e. How many?
	elif pressed == False:
		display.show('#?')
	elif ifStageWait(timeCompare):
		pressed = False
		display.clear()
		stage = 'scoring'

#Scoring with sub functions
def scoring():
	print('reset')


#Ask if want reset.
# Leave on N for 3s to return to scoring.
# Leave on Y for 3s to delete files and reset vars and return to setTeams
def reset():
	print('reset')

#RUN APP
while True:
	if stage == 'start':
		checkFiles()
	elif stage == 'setTeams':
		setTeams()
	elif stage == 'scoring':
		scoring()
	elif stage == 'reset':
		reset()