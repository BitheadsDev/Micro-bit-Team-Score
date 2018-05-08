from microbit import*


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