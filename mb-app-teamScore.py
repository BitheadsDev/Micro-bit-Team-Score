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
def displayScore(activeTeamListItem):
	score = scores[activeTeamListItem]
	#divmod creates two vars
	# The first's value is how many whole times the specified number divides into the value you feed it;
	# the second's value is the remainder one your number has been divided
	#In this case: How many times does 10 go into x (which gives you total 10s); and how much is left over (which gives total 1s)
	tens, ones = divmod(score, 10)
	#Iterate for each tens XY pair in list
	for i, coords in enumerate(tensXY):
		x = coords[0]
		y = coords[1]
		#If item is less than the value of how many tens there are in the score then set that item's LED to on
		if i < tens:
			display.set_pixel(x,y,9)
		#Otherwise set to off
		else:
			display.set_pixel(x,y,0)
	#Iterate for each ones XY pair in list
	for i, coords in enumerate(onesXY):
		x = coords[0]
		y = coords[1]
		if i < ones:
			display.set_pixel(x,y,9)
		else:
			display.set_pixel(x,y,0)

def writeFile(fileName, content):
	#Open file in write mode and write content to it. Overwrites all previous data.
	with open(fileName, 'w') as f:
		f.write(str(content))


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
	global activeTeam
	global totalTeams
	global funcStage
	global stage
	global totalTeams
	global isFiles

	if funcStage == 'start':
		#Show active team
		if activeTeam == 0:
			#On load is the only time activeTeam will be set to 0.
			# On load check if files and if so display the first teams; score
			if isFiles:
				displayScore(activeTeam)
			activeTeam = 1
		#Iterate for each ones XY pair in list
		for i, coords in enumerate(teamsXY):
			x = coords[0]
			y = coords[1]
			#if active team then switch light on otherwise switch light off
			if i == activeTeam - 1:
				display.set_pixel(x,y,9)
			else:
				display.set_pixel(x,y,0)
		funcStage = 'controls'
	else:
		#Increase or decrease score of active team
		if button_b.was_pressed():
			activeTeamListItem = activeTeam - 1
			if scores[activeTeamListItem] < 110:
				scores[activeTeamListItem] += 1
			else:
				display.show('Limit')
			#filename constructed var + number from loop + .txt file extension. 
			# Number from loops needs to be converted to string to be a file name.
			writeFile(scoreFileName + str(activeTeam) + '.txt', scores[activeTeamListItem])
			displayScore(activeTeamListItem)
		elif button_a.was_pressed():
			activeTeamListItem = activeTeam - 1
			if scores[activeTeamListItem] > 0:
				scores[activeTeamListItem] -= 1
			writeFile(scoreFileName + str(activeTeam) + '.txt', scores[activeTeamListItem])
			displayScore(activeTeamListItem)
		#Left and right gestures to switch teams for scoring
		elif accelerometer.was_gesture('right'):
			if activeTeam < totalTeams:
				activeTeam += 1
			else:
				activeTeam = 1
			funcStage = 'start'
			displayScore(activeTeam - 1)
		elif accelerometer.was_gesture('left'):
			if activeTeam > 1:
				activeTeam -= 1
			else:
				activeTeam = totalTeams
			funcStage = 'start'
			displayScore(activeTeam - 1)
		#If Micro"bit is shaken then start reset function
		elif accelerometer.was_gesture('shake'):
			funcStage = 'start'
			stage = 'reset'
			print('shaken')


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