from microbit import*

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

#APP STAGE FUNCTIONS

#Check if the score files exist.
# If they do load them into the list and skip to scoring.
# If they don't then go to setTeams
def checkFiles():

#Ask how many teams need to be scored
def setTeams():

#Scoring with sub functions
def scoring():


#Ask if want reset.
# Leave on N for 3s to return to scoring.
# Leave on Y for 3s to delete files and reset vars and return to setTeams
def reset():

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