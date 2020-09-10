# import the library
import sys
import subprocess
import os
import random
from shutil import rmtree
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
supportedFiles = ['dat', 'zip', 'rar', 'tar', '7z', 'gzip']
supported = False

# create a GUI variable called app
app = gui("Debug Analyzer", "600x600")
app.setResizable(canResize=False)
app.setIcon('img/debug.gif')
app.setFg('white', override=False)
app.setBg('#263238', override=False, tint=False)
app.setFont(size=12, family="Verdana", underline=False, slant="roman")


def launchSubWindow(win):
    app.showSubWindow(win)


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
    #cmdVScode = "code " + destination + name
    cmdVScode = "code " + destination

    result = subprocess.run(cmdVScode, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        print(cmdVScode, 'succ -> ' + result.stdout.decode('utf-8'), 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot run VScode", str(datetime.now()) + " debug analizer: Error occurred while launching VScode \n" + result.stderr.decode('utf-8'))
        # Delete extracted folder in case of error while opening
        if os.path.exists(destination):
            rmtree(destination)


def openWithSub(path, name):
    print('sub :' + path + " with name : " + name)

    # Did this because env PATH is not created for sublime by default on installation,
    # plus didn't know how to use global vars in py so I made the local one here,
    # should change later to directly overwrite in original if
    if isx64():
        sublimeExecutable = '"C:' + bar + 'Program Files' + bar + 'Sublime Text 3' + bar + 'subl.exe"'
    else:
        sublimeExecutable = '"C:' + bar + 'Program Files (x86)' + bar + 'Sublime Text 3' + bar + 'subl.exe"'
    
    cmdSubl = sublimeExecutable + ' -a ' + destination
    result = subprocess.run(cmdSubl, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        print(cmdSubl, 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot run Sublime Text", str(datetime.now()) + " debug analizer: Error occurred while launching Sublime Text 3! \n" + result.stderr.decode('utf-8'))
        # Delete extracted folder in case of error while opening
        if os.path.exists(destination):
            rmtree(destination)


def unZip(path, name):
    print('unzip :' + path + "\nwith name : " + name)
    cmd7z = "7z" + ' x ' + path + ' -bsp1 -o' + destination

    # Lazy way of doing the progress bar
    for x in range(0, 11):
        app.setMeter("progress", x*random.randint(1, 10))

    result = subprocess.run(cmd7z, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        print(cmd7z, 'succ -> ' + result.stdout.decode('utf-8'), 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot extract file", str(datetime.now()) + " debug analizer: Error occurred while extracting file \n" + result.stderr.decode('utf-8') + "\nPlease check if the file is corrupted and try again.")
        app.setMeter("progress", 0)
        return 0
    app.setMeter("progress", 100)



# Events
def btnPress(btn):
    global name
    if btn == 'X':
        clearFileInput()
    else:
        name = app.getEntry("fileName")
        path = app.getEntry("file")

    if btn == 'vscode':
        check(path, btn)

    if btn == 'sublime':
        check(path, btn)
    
    if btn == 'Help':
        os.system('START "" https://github.com/joeperpetua/debug-analyzer#debug-analyzer-docs')

    if btn == 'Report Bug':
        os.system('START "" https://github.com/joeperpetua/debug-analyzer#bug-report')
    
    if btn == 'Close' or btn == ' Close ':
        app.hideAllSubWindows()
    
    if btn == 'Download Visual Studio Code':
        os.system('START "" https://code.visualstudio.com/download')

    if btn == 'Download Sublime Text 3':
        os.system('START "" https://www.sublimetext.com/3')

    if btn == 'Download 7zip':
        os.system('START "" https://www.7-zip.org/download.html')


def check(path, btn):
    global destination
    global name
    # Check path possible scenarios
    if path == '':
        print('please select a file')
        app.warningBox("No file selected", "Please select a file to analyze", parent=None)
        return 0
    elif os.path.exists(path):
        print('path exists')
        for element in supportedFiles:
            if path.endswith(element):
                global supported
                supported = True
                print('file type supported: ' + element)
        
        if not supported:
            app.errorBox("File not supported", "The tool supports only 'dat', 'zip', 'rar', 'tar', '7z', 'gzip' file extensions...\nCheck it")
            return 0

    # C:\tickets\name\
    destination += name + bar

    # Check directory name possible scenarios
    if name == '':
        print('name not set, ticket will be saved with default name')
        name = 'default_' + str(random.randint(0, 999999))
    elif os.path.exists(destination):
        print('Ticket already exists')
        ticketExist = app.questionBox("Existing ticket", "Ticket already exists, do you want to create a subfolder under the existing one to have the two versions?\nIf not, it will be overwritten.", parent=None)
        # Returns True if create a subfolder, False if overwrite
        if ticketExist:
            if os.path.exists(destination + name + "v2"):
                app.warningBox("Existing ticket", "Cannot have more than 2 version, please delete the newer version or change its directory name.", parent=None)
                return 0
        
            print("Create subfolder")
            name += "v2"
            # C:\tickets\name\namev2\
            destination += name + bar
            os.mkdir(destination)
            
        else:
            print("Overwrite")
            pass
        

    # Check if programs are installed
    
    canRun = 0
    #x64
    if isx64():

        #7z64 \\ C:\Program Files\7-Zip\7z.exe
        if os.path.exists('C:' + bar + 'Program Files' + bar + '7-Zip' + bar + '7z.exe'):
            print('7z found')
            canRun += 1
            pass
        else:
            print('7z64 not found')
            launchSubWindow('7zip not found')
            return 0

        #VScode64 \\ C:Users\USER\AppData\Local\Programs\Microsoft VS Code\code.exe
        if os.path.exists('C:' + bar + 'Users' + bar + os.getlogin() + bar + 'AppData' + bar + 'Local' + bar + 'Programs' + bar + 'Microsoft VS Code' + bar + 'code.exe'):
            print('VScode found')
            canRun += 1
            pass
        else:
            print('VScode64 not found')

        #Sublime64 \\ C:\Program Files\Sublime Text 3\subl.exe
        if os.path.exists('C:' + bar + 'Program Files' + bar + 'Sublime Text 3' + bar + 'subl.exe'):
            print('Sublime Text 3 found')
            canRun += 1
            pass
        else:
            print('Sublime Text 3 64 not found')
            if canRun <= 1:
                launchSubWindow('Text editor not found')
                return 0
    #x86
    else:
        
        #7z86 \\ C:\Program Files (x86)\7-Zip\7z.exe 
        if os.path.exists('C:' + bar + 'Program Files (x86)' + bar + '7-Zip' + bar + '7z.exe'):
            print('7z found')
            canRun += 1
            pass
        else:
            print('7z not found')
            launchSubWindow('7zip not found')
            return 0

        #VScode
        if os.path.exists('C:' + bar + 'Users' + bar + os.getlogin() + bar + 'AppData' + bar + 'Local' + bar + 'Programs' + bar + 'Microsoft VS Code' + bar + 'code.exe'):
            print('VScode found')
            canRun += 1
            pass
        else:
            print('VScode not found')

        #Sublime86  \\ C:\Program Files (x86)\Sublime Text 3\subl.exe 
        if os.path.exists('C:' + bar + 'Program Files (x86)' + bar + 'Sublime Text 3' + bar + 'subl.exe'):
            print('Sublime Text 3 found')
            canRun += 1
            pass
        else:
            print('Sublime Text 3 not found')
            if canRun <= 1:
                launchSubWindow('Text Editor not found')
                return 0
        
    if unZip(path, name) == 0:
        return 0
    
    if app.getRadioButton("debug") == "Move debug file to extracted folder":
        print("moveDebug")
        os.replace(path, destination  + name + ".dat")

    if app.getRadioButton("debug") == "Delete debug file after extracting it\n(the extracted directory will remain)":
        print("delDebug")
        os.remove(path)
    
    if app.getCheckBox("openDebug"):
        os.system('START "" http://192.168.40.40/debug/')

    if btn == 'vscode':
        openWithVS(path, name)

    if btn == 'sublime':
        openWithSub(path, name)  

    destination = "C:" + bar + "tickets" + bar
  

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
    #app.setEntryTooltip("fileName", "If no name is provided a random name will be assigned")
    # File input
    app.addLabel("file label", "Select debug file", row=1, column=0, colspan=2)
    app.setPadding([5,5])
    app.addFileEntry("file", row=1, column=3, colspan=1)
    app.addButton("X", btnPress, row=1, column=4)
    app.setButtonBg("X", "#e5806c")
    app.setButtonRelief("X", "flat")
    app.setPadding([0,0])
    app.stopFrame()

    app.startFrame('choice')
    app.setFg('grey', override=False)
    app.setSticky("w")
    app.addRadioButton("debug", "Move debug file to extracted folder")
    app.addRadioButton("debug", "Delete debug file after extracting it\n(the extracted directory will remain)")
    app.addNamedCheckBox("Open the debug analyzer tool in a new browser\nwindow (you will need the debug file to do so)", "openDebug")
    app.stopFrame()

    # app.addCheckBox("Delete debug file after extracting it (the extracted directory will remain)")
    # app.addCheckBox("Open the debug analyzer tool in a new browser window")

    app.startFrame("buttons", row=3, column=0)
    app.setSticky("ew")
    app.setFg('white', override=False)
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

    # --------------
    # SUBWINDOWS
    # --------------

    app.startSubWindow('7zip not found', modal=True)
    app.setBg('#263238', override=False, tint=False)
    app.setPadding([60,60])

    app.startFrame('modal 7z', row=0, column=0)
    app.addLabel("7zip not found message", "The program 7zip was not found in your system, this is a required\nprogram to run the tool, please install it and try launching the tool again.", row=0, column=0)
    app.stopFrame()

    app.startFrame('modal 7z2', row=1, column=0)
    app.setPadding([60,10])
    app.addButton('Download 7zip', btnPress, row=0, column=0)
    app.addButton('Close', btnPress, row=0, column=1)
    app.stopFrame()

    app.stopSubWindow()

    app.startSubWindow('Text editor not found', modal=True)
    app.setBg('#263238', override=False, tint=False)
    app.setPadding([60,60])

    app.startFrame('modal te', row=0, column=0)
    app.addLabel("Lb not found message", "The tool could not find nor Visual Studio Code nor Sublime Text 3,\nat least one of them is required to run the tool,\nplease install either of them and try launching the tool again.", row=0, column=0)
    app.stopFrame()

    app.startFrame('modal te2', row=1, column=0)
    app.setPadding([60,10])
    app.addButton('Download Visual Studio Code', btnPress, row=0, column=0)
    app.addButton('Download Sublime Text 3', btnPress, row=0, column=1)
    app.addButton(' Close ', btnPress, row=0, column=2)
    app.stopFrame()

    app.stopSubWindow()

    # start the GUI
    app.go()
