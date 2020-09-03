# import the library
import sys
import subprocess
import os
import random
from os import sep as bar
from datetime import datetime
from shutil import copyfile
from appJar import gui
sevenZipExecutable = "7z"
codeExecutable = "code"
# Sublime is not set by default in PATH so it will be executed from
# the .exe path that is installed on the PC, the var will be overwritten in the arch check
sublimeExecutable = ""
destination = "C:" + bar + "tickets" + bar
name = ''
path = ''

# create a GUI variable called app
app = gui("Debug Analyzer", "600x600")
app.setResizable(canResize=False)
app.setIcon('img/debug.gif')
app.setFg('white', override=False)
app.setBg('#263238', override=False, tint=False)
app.setFont(size=12, family="Verdana", underline=False, slant="roman")



def isx64():
    if 'PROCESSOR_ARCHITEW6432' in os.environ:
        return True
    return os.environ['PROCESSOR_ARCHITECTURE'].endswith('64')


def clearFileInput():
    print('clear file')
    app.clearEntry("file")
    app.setMeter("progress", 0)


def openWithVS(path, name):
    print('vs :' + path + " with name : " + name)   
    cmdVScode = "code " + destination + name
    try:
        os.system(cmdVScode)
    except Exception as err:
        print(str(datetime.now()) + " debug analizer: Error occurred while launching VScode! \n")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Type error: " + str(err))
        print('File Name:', fname, 'Line Numer:', exc_tb.tb_lineno, end = '\n\n')   


def openWithSub(path, name):
    print('sub :' + path + " with name : " + name)

    if isx64():
        sublimeExecutable = '"C:' + bar + 'Program Files' + bar + 'Sublime Text 3' + bar + 'subl.exe"'
    else:
        sublimeExecutable = '"C:' + bar + 'Program Files (x86)' + bar + 'Sublime Text 3' + bar + 'subl.exe"'
    
    cmdSubl = sublimeExecutable + ' -a ' + destination + name
    try:
        os.system(cmdSubl)
    except Exception as err:
        print(str(datetime.now()) + " debug analizer: Error occurred while launching VScode! \n")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Type error: " + str(err))
        print('File Name:', fname, 'Line Numer:', exc_tb.tb_lineno, end = '\n\n')    


    # cmdSubl = sublimeExecutable + ' -a ' + destination + name
    # try:
    #     os.system(cmdSubl)
    # except Exception as err:
    #     print(str(datetime.now()) + " debug analizer: Error occurred while launching VScode! \n")
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print("Type error: " + str(err))
    #     print('File Name:', fname, 'Line Numer:', exc_tb.tb_lineno, end = '\n\n')     


def unZip(path, name):
    print('unzip :' + path + "\nwith name : " + name)
    cmd7z = "7z" + ' x ' + path + ' -bsp1 -o' + destination + name
    try:
        for x in range(0, 11):
            app.setMeter("progress", x*random.randint(1, 10))
        os.system(cmd7z)
        app.setMeter("progress", 100)
    except Exception as err:
        print(str(datetime.now()) + " debug analizer: Error occurred while extracting file! \n")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Type error: " + str(err))
        print('File Name:', fname, 'Line Numer:', exc_tb.tb_lineno, end = '\n\n')


# Events
def btnPress(btn):
    if btn == 'X':
        clearFileInput()
    else:
        name = app.getEntry("fileName")
        path = app.getEntry("file")

    if btn == 'vscode':
        check(path, name, btn)
        #openWithVS(path, name)

    if btn == 'sublime':
        check(path, name, btn)
        #openWithSub(path, name)  


def check(path, name, btn):
    # Check path possible scenarios
    if path == '':
        print('please select a file')
        app.warningBox("No file selected", "Please select a file to analyze", parent=None)
        return 0
    elif os.path.exists(path):
        print('path is valid')
    
    # Check directory name possible scenarios
    if name == '':
        print('name not set, ticket will be saved with default name')
        name = 'default_' + str(random.randint(0, 999999))
    elif os.path.exists(destination + name):
        print('Ticket already exists')
        app.warningBox("Existing ticket", "Ticket already exists, please try with another custom name", parent=None)
        return 0

    # Check if programs are installed
    
    #x64
    if isx64():

        #7z64 \\ C:\Program Files\7-Zip\7z.exe
        if os.path.exists('C:' + bar + 'Program Files' + bar + '7-Zip' + bar + '7z.exe'):
            print('7z found')
            pass
        else:
            print('7z64 not found')
            return 0

        #VScode64 \\ C:Users\USER\AppData\Local\Programs\Microsoft VS Code\code.exe
        if os.path.exists('C:' + bar + 'Users' + bar + os.getlogin() + bar + 'AppData' + bar + 'Local' + bar + 'Programs' + bar + 'Microsoft VS Code' + bar + 'code.exe'):
            print('VScode found')
            pass
        else:
            print('VScode64 not found')
            return 0

        #Sublime64 \\ C:\Program Files\Sublime Text 3\subl.exe
        if os.path.exists('C:' + bar + 'Program Files' + bar + 'Sublime Text 3' + bar + 'subl.exe'):
            print('Sublime Text 3 found')
            pass
        else:
            print('Sublime Text 3 64 not found')
            return 0
    #x86
    else:
        
        #7z64 \\ C:\Program Files (x86)\7-Zip\7z.exe 
        if os.path.exists('C:' + bar + 'Program Files (x86)' + bar + '7-Zip' + bar + '7z.exe'):
            print('7z found')
            pass
        else:
            print('7z not found')
            return 0

        #VScode64
        if os.path.exists('C:' + bar + 'Users' + bar + os.getlogin() + bar + 'AppData' + bar + 'Local' + bar + 'Programs' + bar + 'Microsoft VS Code' + bar + 'code.exe'):
            print('VScode found')
            pass
        else:
            print('VScode not found')
            return 0

        #Sublime64  \\ C:\Program Files (x86)\Sublime Text 3\subl.exe 
        if os.path.exists('C:' + bar + 'Program Files (x86)' + bar + 'Sublime Text 3' + bar + 'subl.exe'):
            print('Sublime Text 3 found')
            pass
        else:
            print('Sublime Text 3 not found')
            return 0
        
    unZip(path, name)

    if btn == 'vscode':
        openWithVS(path, name)

    if btn == 'sublime':
        openWithSub(path, name)  
    
  

# Render GUI
if app:
    #app.setSticky("news")
    #app.setExpand("both")
    app.setStretch("both")


    app.startFrame("header", row=0, column=0)
    app.addLabel("l1", " ", row=0, column=0, colspan=1, rowspan=1)
    app.addLabel("l2", "Select a .dat debug file to open with VScode or Sublime Text 3", row=0, column=1, colspan=1, rowspan=1)
    app.addLabel("l4", " ", row=0, column=2, colspan=1, rowspan=1)
    app.stopFrame()

    app.setPadding([60,10])
    app.startFrame("body", row=1, column=0, colspan=4, rowspan=1)
    app.setPadding([0,0])

    # File name input
    app.setSticky("ew")
    app.addLabel("name label", "Ticket n.", row=0, column=0, colspan=2)
    app.addEntry("fileName", row=0, column=3)
    app.setEntryRelief("fileName", "groove")
    app.setEntryTooltip("fileName", "If no name is provided a random name will be assigned")
    # File input
    app.addLabel("file label", "Select debug file", row=1, column=0, colspan=2)
    app.setPadding([5,5])
    app.addFileEntry("file", row=1, column=3, colspan=1)
    app.addButton("X", btnPress, row=1, column=4)
    app.setButtonBg("X", "#e5806c")
    app.setButtonRelief("X", "flat")
    app.setPadding([0,0])
    app.stopFrame()


    app.startFrame("buttons", row=3, column=0)
    app.addLabel("Choose", "Open with:", row=0, column=0)
    app.addButtons(["vscode", "sublime"], btnPress,row=1, column=0,)
    app.setButtonImage("vscode", "img/vscode.gif")
    app.setButtonBg("vscode", "#192227")
    app.setButtonRelief("vscode", "flat")

    app.setButtonImage("sublime", "img/sublime.gif")
    app.setButtonBg("sublime", "#192227")
    app.setButtonRelief("sublime", "flat")
    # app.setPadding([60,100])
    app.addMeter("progress", row=2, column=0)
    app.setMeterFill("progress", "#192227")
    app.setPadding([0,0])
    app.stopFrame()

    app.startFrame("footer", row=4, column=0)
    app.setSticky("w")
    app.addButton("Help", btnPress, row=0, column=0, colspan=1)
    app.setButtonBg("Help", "#4a4e50")
    app.setButtonFg("Help", "#ffffff")
    app.setButtonRelief("Help", "flat")
    app.setSticky("ew")
    app.addImage("logo", "img/logo.gif", row=0, column=1, colspan=2, rowspan=1)
    app.setSticky("e")
    app.addButton("Report Bug", btnPress, row=0, column=3, colspan=1)
    app.setButtonBg("Report Bug", "#4a4e50")
    app.setButtonFg("Report Bug", "#ffffff")
    app.setButtonRelief("Report Bug", "flat")
    app.stopFrame()


    # start the GUI
    app.go()
