from tkinter import *
import ctypes
import random
import tkinter
 
# For a sharper window
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Setup
root = Tk()
root.title('Type Speed Test')

# Setting the starting window dimensions
root.geometry('700x700')

# Setting the Font for all Labels and Buttons
root.option_add("*Label.Font", "consolas 30")
root.option_add("*Button.Font", "consolas 30")


# functions
def keyPress(event=None):
    try:
        if event.char.lower() == labelRight.cget('text')[0].lower():
            # Deleting one from the right side.
            labelRight.configure(text=labelRight.cget('text')[1:])
            # Deleting one from the right side.
            labelLeft.configure(text=labelLeft.cget('text') + event.char.lower())
            #set the next Letter Lavbel
            currentLetterLabel.configure(text=labelRight.cget('text')[0])
    except:
        pass


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
    global HSget
    HSget=open('Highscore.txt','r+')
    global High
    High=max(int(i) for i in HSget.read().split('\n'))
    #highscore
    global HS
    HS=Label(root, text=f'Current highscore is {High} wpm \n global highscore is 212 wpm', fg='black')
    HS.place(relx=0.5, rely=0.2, anchor=N)
    global Timeget
    Timeget=Label(root, text='Please enter the time (number of minutes to practice) between 1-10', fg='black')
    Timeget.place(relx=0.5, rely=0.4, anchor=N)
    #taking the amount of time user wants to use the app
    global Time
    Time= Entry(root, width= 40)
    Time.place(relx=0.5,rely=0.5, anchor=N)
    global TimeButton
    TimeButton= Button(root, text=f'Start', command=validatestart)
    TimeButton.place(relx=0.5,rely=0.7,anchor=S)

# this will check if user wrote the correct text
def validatestart():
    if int(Time.get())>0 and int(Time.get())<11:
        global Nominutes
        Nominutes=int(Time.get())
        HS.destroy()
        Timeget.destroy()
        Time.destroy()
        TimeButton.destroy()
        resetWritingLabels()
        
    else:
        HS.destroy()
        Timeget.destroy()
        Time.destroy()
        TimeButton.destroy()
        start()

            

# This will start the Test
start()
# Start the mainloop
root.mainloop()
