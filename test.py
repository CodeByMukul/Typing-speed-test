from tkinter import *
from tkinter import font as font
import ctypes
import random

# For a sharper window

# Setup
root = Tk()
root.title('Type Speed Test')

# Setting the starting window dimensions
root.geometry('700x700')

# Setting the Font for all Labels and Buttons
root.option_add("*Label.Font", "consolas 30")
root.option_add("*Button.Font", "consolas 30")
#improve this
Custom_font = font.Font( family = "Comic Sans MS", size = 30)

# functions
def changeOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))
    
def keyPress(event=None):
    try:
        if event.char.lower() == labelRight.cget('text')[0].lower():
            # Deleting one from the right side.
            labelRight.configure(text=labelRight.cget('text')[1:])
            # Deleting one from the right side.
            labelLeft.configure(text=labelLeft.cget('text') + event.char.lower())
            #set the next Letter Lavbel
            currentLetterLabel.configure(text=labelRight.cget('text')[0])
        else:
            currentLetterLabel.configure(text=currentLetterLabel.cget('text'), fg='red')
            root.after(250, oneLine)

    except:
        pass
def oneLine():
        currentLetterLabel.configure(text=currentLetterLabel.cget('text'), fg='grey')



def resetWritingLabels():
    # Text List
    TextToType=open('sen_type.txt')
    Words=TextToType.read()
    TextToType.close()
    possibleTexts=Words.split('\n')
    text=''
    # Chosing one of the texts randomly with the choice function
    while len(text.split())<220*Nominutes:
        text += random.choice(possibleTexts).lower()
    # defining where the text is split
    splitPoint = 0
    # This is where the text is that is already written
    global labelLeft
    labelLeft = Label(root, text=text[0:splitPoint], fg='grey')
    labelLeft.place(relx=0.5, rely=0.5, anchor=E)

    # Here is the text which will be written
    global labelRight
    labelRight = Label(root, text=text[splitPoint:])
    labelRight.place(relx=0.5, rely=0.5, anchor=W)

    # This label shows the user which letter he now has to press
    global currentLetterLabel
    currentLetterLabel = Label(root, text=text[splitPoint], fg='grey')
    currentLetterLabel.place(relx=0.5, rely=0.6, anchor=N)

    # this label shows the user how much time has gone by
    global timeleftLabel
    timeleftLabel = Label(root, text=f'0 Seconds', fg='grey')
    timeleftLabel.place(relx=0.5, rely=0.4, anchor=S)

    global goal
    goal= Label(root, text=f'Current highscore to beat: {High} wpm \n Number of words to beat: {int(High)*Nominutes}', fg='red')
    goal.place(relx=0.5, rely=0.2, anchor=N)

    global writeAble
    writeAble = True
    root.bind('<Key>', keyPress)

    global passedSeconds
    passedSeconds = 0

    # Binding callbacks to functions after a certain amount of time.
    root.after(Nominutes*60000, stopTest)
    root.after(1000, addSecond)

def stopTest():
    global writeAble
    writeAble = False
    
    # Calculating the amount of words
    global amountWords
    #amountWords = len(labelLeft.cget('text').split(' '))//Nominutes
    amountWords = len(labelLeft.cget('text').split(' '))//Nominutes
    # Destroy all unwanted widgets.
    timeleftLabel.destroy()
    currentLetterLabel.destroy()
    labelRight.destroy()
    labelLeft.destroy()
    goal.destroy()

    #check for hs
    global Cong
    if int(amountWords)>212:
        Cong=Label(root, text=f'Conratulations! You have set a new world record of {amountWords} words per minute.', fg='green')
        Cong.place(relx=0.5, rely=0.2, anchor=N)
        HSget.write('\n'+str(amountWords))
        HSget.close()
    elif int(amountWords)>int(High):
        Cong=Label(root, text=f'Conratulations! You have set a new highscore of {amountWords} words per minute.', fg='green')
        Cong.place(relx=0.5, rely=0.2, anchor=N)
        HSget.write('\n'+str(amountWords))
        HSget.close()
    # Display the test results with a formatted string
    global ResultLabel
    ResultLabel = Label(root, text=f'Words per Minute: {amountWords}', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Display a button to restart the game
    global ResultButton
    ResultButton = Button(root, text=f'Retry', command=restart)
    ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)
    changeOnHover(ResultButton,'grey','#efefef')

def restart():
    # Destry result widgets
    if int(amountWords)>int(High):
        Cong.destroy()
    ResultLabel.destroy()
    ResultButton.destroy()

    # re-setup writing labels.
    start()

def addSecond():
    # Add a second to the counter.

    global passedSeconds
    passedSeconds += 1
    timeleftLabel.configure(text=f'{passedSeconds} Seconds')

    # call this function again after one second if the time is not over.
    if writeAble:
        root.after(1000, addSecond)
def start():
    multiP.destroy()
    singleP.destroy()
    global HSget
    HSget=open('Highscore.txt','r+')
    global High
    High=max(int(i) for i in HSget.read().split('\n'))
    #highscore
    global HS
    HS=Label(root, text=f'Current highscore is {High} wpm \n Global highscore is 212 wpm', fg='black', font=Custom_font)#bg='white'
    HS.place(relx=0.5, rely=0.15, anchor=N)
    global Timeget
    Timeget=Label(root, text='Please enter the time (number of minutes to practice) between 1-10', fg='black')
    Timeget.place(relx=0.5, rely=0.4, anchor=N)
    #taking the amount of time user wants to use the app
    global Time
    Time= Entry(root, width= 40)
    Time.place(relx=0.5,rely=0.5, anchor=N)
    global TimeButton
    TimeButton= Button(root, text=f'Start',width=6, command=validatestart)
    TimeButton.place(relx=0.5,rely=0.7,anchor=S)
    changeOnHover(TimeButton,'green','#efefef')
    global backButton
    backButton= Button(root,text='Back',width=6, command=sBack)
    backButton.place(relx=0.5,rely=0.82,anchor=S)
    changeOnHover(backButton,'red','#efefef')

# this will check if user wrote the correct text for the time input
def validatestart():
    if int(Time.get())>0 and int(Time.get())<11:
        global Nominutes
        Nominutes=int(Time.get())
        HS.destroy()
        Timeget.destroy()
        Time.destroy()
        TimeButton.destroy()
        backButton.destroy()
        resetWritingLabels()
        
    else:
        HS.destroy()
        Timeget.destroy()
        Time.destroy()
        TimeButton.destroy()
        backButton.destroy()
        start()

def sBack():
    backButton.destroy()
    HS.destroy()
    Timeget.destroy()
    Time.destroy()
    TimeButton.destroy()
    homeScreen()

def mBack():
    backButton.destroy()
    noPlayers.destroy()
    players.destroy()
    playButton.destroy()
    homeScreen()

def mStart():
    multiP.destroy()
    singleP.destroy()
    try:
        backAgainButton.destroy()
        headingLabel.destroy() 
        rule1Label.destroy()
        rule2Label.destroy()
        rule3Label.destroy()
        rule4Label.destroy()

    except:pass
    global turn
    turn=0
    global mHigh
    mHigh=0
    global turn_over
    turn_over=0
    global noPlayers
    noPlayers=Label(root, text='Please enter the number of players', fg='black')
    noPlayers.place(relx=0.5, rely=0.3, anchor=N)
    #taking the amount of players that want to compete 
    global players
    players= Entry(root, width= 40)
    players.place(relx=0.5,rely=0.4, anchor=N)
    global playButton
    playButton= Button(root, text=f'Play',width=6, command=validatemStart)#! DO NOT RUN, COMMAND ME BAS AISE HI KUCH BHI DAAL DIA HAI
    playButton.place(relx=0.5,rely=0.6,anchor=S)
    changeOnHover(playButton,'green','#efefef')
    global backButton
    backButton= Button(root,text='Back',width=6, command=mBack)
    backButton.place(relx=0.5,rely=0.84,anchor=S)
    changeOnHover(backButton,'red','#efefef')
    global guideButton
    guideButton= Button(root,text='Guide',width=6, command=mGuide)
    guideButton.place(relx=0.5,rely=0.72,anchor=S)
    changeOnHover(guideButton,'blue','#efefef')

def validatemStart():
    if int(players.get())>1:
        playerTurn()



def mGuide():
    noPlayers.destroy()
    players.destroy()
    playButton.destroy()
    backButton.destroy()
    guideButton.destroy()
    global headingLabel
    headingLabel=Label(root, text='Guide', fg='black', font='consolas 30 bold')
    headingLabel.place(relx=0.5, rely=0.05, anchor=N)
    global rule1Label 
    rule1Label=Label(root, text='1)Minimum 2 players are required to play this game mode', fg='black', font='consolas 20')
    rule1Label.place(relx=0.268, rely=0.2, anchor=N)
    global rule2Label
    rule2Label=Label(root, text='2)Each player will get one minute to type', fg='black', font='consolas 20')
    rule2Label.place(relx=0.2, rely=0.3, anchor=N)
    global rule3Label
    rule3Label=Label(root, text='3)Incase of rematch, the highest score will be saved to beat', fg='black', font='consolas 20')
    rule3Label.place(relx=0.292, rely=0.4, anchor=N)
    global rule4Label
    rule4Label=Label(root, text='Good Luck!', fg='black', font='consolas 30 bold')
    rule4Label.place(relx=0.5, rely=0.55, anchor=N)
    global backAgainButton
    backAgainButton= Button(root,text='Back',width=6, command=mStart)
    backAgainButton.place(relx=0.5,rely=0.84,anchor=S)
    changeOnHover(backAgainButton,'red','#efefef')
    
    pass



def multiHigh(i):
    global mHigh
    mHigh=i

'''
def multiStart():#!iski wajah se shayad countdown me dikkat aa rhi hai will have to see
    n=1
    play=int(players.get())
    while n<=play:
        n=playerTurn(n)
'''
def homeScreen():
    global multiP
    multiP=Button(root, text='Multiplayer', fg='black',height=3,width=30, command=mStart)
    multiP.place(relx=0.5,rely=0.5,anchor=N)
    changeOnHover(multiP,'grey','#efefef')
    global singleP       
    singleP=Button(root, text='Singleplayer/Practice', fg='black',height=3,width=30, command=start)
    singleP.place(relx=0.5,rely=0.2,anchor=N)
    changeOnHover(singleP,'grey','#efefef')

def multiResetWritingLabels():
    # Text List
    playerNo.destroy()
    countdownLabel.destroy()
    TextToType=open('sen_type.txt')
    Words=TextToType.read()
    TextToType.close()
    possibleTexts=Words.split('\n')
    text=''
    # Chosing one of the texts randomly with the choice function
    while len(text.split())<220*1:
        text += random.choice(possibleTexts).lower()
    # defining where the text is split
    splitPoint = 0
    # This is where the text is that is already written
    global labelLeft
    labelLeft = Label(root, text=text[0:splitPoint], fg='grey')
    labelLeft.place(relx=0.5, rely=0.5, anchor=E)

    # Here is the text which will be written
    global labelRight
    labelRight = Label(root, text=text[splitPoint:])
    labelRight.place(relx=0.5, rely=0.5, anchor=W)

    # This label shows the user which letter he now has to press
    global currentLetterLabel
    currentLetterLabel = Label(root, text=text[splitPoint], fg='grey')
    currentLetterLabel.place(relx=0.5, rely=0.6, anchor=N)

    # this label shows the user how much time has gone by
    global timeleftLabel
    timeleftLabel = Label(root, text=f'0 Seconds', fg='grey')
    timeleftLabel.place(relx=0.5, rely=0.4, anchor=S)
    global goal
    if turn==1 and mHigh==0:
        goal= Label(root, text=f'You are the first player! Try setting a highscore no one can beat!', fg='red')
        goal.place(relx=0.5, rely=0.2, anchor=N)
    else:  
        goal= Label(root, text=f'Current highscore to beat: {mHigh} wpm \n Type the words written below!', fg='red')
        goal.place(relx=0.5, rely=0.2, anchor=N)

    global writeAble
    writeAble = True
    root.bind('<Key>', keyPress)

    global passedSeconds
    passedSeconds = 0

    # Binding callbacks to functions after a certain amount of time.
    root.after(5000, multiStopTest)
    root.after(1000, addSecond)

def playerTurn():
    global turn_over
    if turn_over>0:
        pass
    else:
        turn_over=int(players.get())
    try:
        noPlayers.destroy()
        players.destroy()
        playButton.destroy()
        backButton.destroy()
        guideButton.destroy()
        ResultLabel.destroy()
        Cong.destroy()
        ResultButton.destroy()
    except:
        pass
    global turn
    turn+=1
    if turn>turn_over:
        endTest()
    else:
        global playerNo
        playerNo=Label(root, text=f"Player {turn}'s turn begins in", fg='black')
        playerNo.place(relx=0.5, rely=0.4, anchor=N)



        global countdown
        countdown=11

        #root.after(1000, countdownMulti)
        root.after(1000,countdownMulti())



def countdownMulti():
    global countdown
    # countdown 1 second at  a time.
    global countdownLabel
    if countdown==11:
        countdownLabel = Label(root, text=f'10 Seconds', fg='grey')
        countdownLabel.place(relx=0.5, rely=0.6, anchor=S)
    countdown -= 1
    countdownLabel.configure(text=f'{countdown} Seconds')

    # call this function again after one second if the time is not over.
    if countdown>0:
        root.after(1000,countdownMulti)
    else:
        countdown=11
        multiResetWritingLabels()

def multiStopTest():
    global writeAble
    writeAble = False
    
    # Calculating the amount of words
    global amountWords
    #amountWords = len(labelLeft.cget('text').split(' '))//Nominutes
    amountWords = len(labelLeft.cget('text').split(' '))
    # Destroy all unwanted widgets.
    timeleftLabel.destroy()
    currentLetterLabel.destroy()
    labelRight.destroy()
    labelLeft.destroy()
    goal.destroy()

    #check for hs
    global Cong
    global mHigh
    global turn
    if int(amountWords)>212:
        Cong=Label(root, text=f'Conratulations! You have set a new world record of {amountWords} words per minute.', fg='green')
        Cong.place(relx=0.5, rely=0.2, anchor=N)
        HSget.write('\n'+str(amountWords))
        HSget.close()
    elif int(amountWords)>int(mHigh):
        Cong=Label(root, text=f'Conratulations! You have set a new highscore of {amountWords} words per minute.', fg='green')
        Cong.place(relx=0.5, rely=0.2, anchor=N)
        mHigh=int(amountWords)
        global winturn
        winturn=turn
    # Display the test results with a formatted string
    global ResultLabel
    ResultLabel = Label(root, text=f'Words per Minute: {amountWords}', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    global ResultButton
    ResultButton = Button(root, text=f'Next', command=playerTurn)
    ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)
    changeOnHover(ResultButton,'grey','#efefef')

def endTest():
    global winturn
    global ResultLabel
    ResultLabel = Label(root, text=f'The winner is Player {winturn} with a score of {mHigh} words per minute!', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
    #changeonhover function use krna koi button add kro toh
    #! change time of test from 10 seconds to 60 seconds
    global playAgainButton
    playAgainButton = Button(root, text=f'Rematch', command=mRestart)
    playAgainButton.place(relx=0.5, rely=0.65, anchor=CENTER)
    changeOnHover(playAgainButton,'grey','#efefef')

    global exitButton
    exitButton = Button(root, text=f'Back', command=mEnd)
    exitButton.place(relx=0.5, rely=0.8, anchor=CENTER)
    changeOnHover(exitButton,'red','#efefef')

def mEnd():
    ResultLabel.destroy()
    playAgainButton.destroy()
    exitButton.destroy()
    homeScreen()

def mRestart():
    ResultLabel.destroy()
    playAgainButton.destroy()
    exitButton.destroy()
    global turn
    turn=0
    playerTurn()





#! change the time to 60 seconds again add leaderboard?



# This will start the Test
homeScreen()
# Start the mainloop
root.mainloop()
