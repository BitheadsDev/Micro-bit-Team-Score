# Team score Micro:bit App

## Aims of the app

To keep track of up to five teams' scores

## View videos

* Part one – showing the app in action: https://www.youtube.com/watch?v=epTNY8UVVE8
* Part two – talking through the code: https://www.youtube.com/watch?v=wJzbub2Jd-Q

## Details and controls

* You can select up to five teams
* Increase score using B button
* Decrease score using A button
* Tilting the device to the left will shift the team selection -1
* Tilting the device to the right will shift the team selection + 1
* We will save scores to files to allow power off and on to resume scoring
* Shaking the device would prompt a reset request and deletion of files.

## Things you need

* A Micro:bit
* A USB lead
* A computer to copy and write the code

## Things you should learn

* Create a multi-stage application that passes data from one stage to another
* Creating persistent save files that restore data on startup
* Looping through lists to turn appropriate LEDs on and off
* Timed actions
* Using buttons and gestures to control data
* How to display lots of data in a compact format
* How to reset the device by making a selection

## The display

Due to only having a 25x25 screen resolution we have to be creative with our representation:

* First row (horizontal) of five pixels will show team number e.g. if X,Y pixels `[1,0]` are lit up this would be team 2; `[2,0]` = team 3
* The second and third rows of pixels would represent 10s e.g. `[0,1], [1,1], [2,1] = 30`. This means we could represent up to 100 using this method.
* The forth and fifth rows of pixels would represent 1s e.g. `[0,3], [1,3], [2,3], [3,3], [3,4], [4,0] = 6`

## Initial pseudocode runthrough

```
If previous save files:
    Read files and populate totalTeams and scoreTeam1, scoreTeam2 etc variables
else:
    setTeams:
        if B was pressed:
            increment (+=1) totalTeams by 1 up to 5 and display
            if > 5: (if more than five loop back round to 1)
                set and display totalTeams to 1
        if A was pressed:
            decrement (-=1) totalTeams by 1 down to 1 and display
            if < 1: (if less than one set to five)
                set totalTeams to 5

    if no button have been pressed for 3000 seconds:
        Set: totalTeams
        Call: createFiles
        Call: scoring (Jump to next stage)

scoring:
    showActiveTeam
        activeTeam = 1
    if B was pressed:
        +=1 activeTeams' score up to a maximum of 110
        Call: writeFile
        Call: scoreDisplay
    else if A was pressed:
        -=1 activeTeams' score down to a minimum of 0
        Call writeFile
        Call: scoreDisplay
    if shaken:
        Call: reset
    else if tilt right:
        if activeTeam < totalTeams:
            += activeTeam
        else:
            activeTeam = 1
        Call: scoreDisplay
    else if tilt left:
        if activeTeam > 0:
            -= activeTeam
        else:
            activeTeam = totalTeams
        Call: scoreDisplay

scoreDisplay:
    splitUnits:
        Split activeTeams' score into 10s and 1s
    displayTeamRow:
        Light up row 0 with active teams' number e.g. 2,0 would be team 3
    displayTens:
        Light up rows 1+2 activeTeams' 10s score
    displayOnes:
        Light up rows 3+4 with activeTeams' 1s score

createFiles:
    for each team:
        create file e.g. scoreTeam1.txt, scoreTeam2.txt

writeFile:
    write activeTeam file score

reset:
    if 'N' is selected:
        No button pressed for 3000 seconds:
            Call: scoring (Go back to scoring as no reset required)
    else if 'Y' is selected:
        No button has been pressed for 3000 seconds:
            delete all files
            Call: setTeams (loop to beginning)
```

## Possible extensions

* Discuss the limitations of this program.
* Is there a better way of representing teams and the score?
* How could we represent more than five teams?
* How could we represent a score of more than 110?