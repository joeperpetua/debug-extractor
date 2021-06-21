# import the library
import sys
import subprocess
import os
import random
import config
import yaml
from os import sep as bar
from shutil import rmtree
from datetime import datetime
from shutil import copyfile
from appJar import gui
from pathlib import Path

with open("config.yml", "r") as ymlfile:
    conf = yaml.load(ymlfile, Loader=yaml.FullLoader)

sevenZipExecutable = ""
codeExecutable = ""
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
app.setLogFile('daemon.log')

def launchSubWindow(win):
    app.showSubWindow(win)

def openSettings():
    app.hideAllSubWindows()
    subprocess.run("notepad config.yml", shell=True)
    #app.showSubWindow('Settings')
    app.info("settings file opened")

# def isx64():
#     if 'PROCESSOR_ARCHITEW6432' in os.environ:
#         return True
#     return os.environ['PROCESSOR_ARCHITECTURE'].endswith('64')

def clearFileInput():
    app.clearEntry("file")
    app.setMeter("progress", 0)
    app.info("File input cleared")


def openWithVS(path, name):
    print('vs :' + path + " with name : " + name)   
    cmdVScode = "code " + destination
    print(cmdVScode)
    # cmdVScode = '"' + codeExecutable + '" ' + destination

    formated_vs_PATH = Path(codeExecutable + "/bin")
    env_path = os.environ.get('PATH', 'No PATH env variable')

    # print("vs pathhhhasdhha" + str(formated_vs_PATH))
    # print("epath ---------- " + env_path)
    app.info("Opening VScode...")
    print("Opening VScode...")

    # check for env PATH for vs code and errors if not found
    if str(formated_vs_PATH) in env_path:
        print("env path for code found")
        app.info("env path for code found")
    else:
        launchSubWindow("ENV variable for VS Code not found")
        print("env path for code not found")
        app.error("env path for code not found")
        # Delete extracted folder in case of error while opening
        if os.path.exists(destination):
            rmtree(destination)
        return 0
    
    # uses the env PATH to open vscode, if error print and delete extracted directory
    result = subprocess.run(cmdVScode, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    app.info("VScode result : " + str(result))

    if result.stderr:
        print(cmdVScode, 'succ -> ' + result.stdout.decode('utf-8'), 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot run VScode", str(datetime.now()) + " debug analizer: Error occurred while launching VScode \n" + result.stderr.decode('utf-8'))
        app.error("Cannot run VScode /// " + str(datetime.now()) + " /// debug analizer: Error occurred while launching VScode /// " + result.stderr.decode('utf-8'))
        # Delete extracted folder in case of error while opening
        if os.path.exists(destination):
            rmtree(destination)
        return 0

    app.info("VScode opened !")
    print("VScode opened !")


def openWithSub(path, name):
    print('sub :' + path + " with name : " + name)
    
    cmdSubl = '"' + sublimeExecutable + '" -a ' + destination
    app.info("Opening Sublime...")
    result = subprocess.run(cmdSubl, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        print(cmdSubl, 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot run Sublime Text", str(datetime.now()) + " debug analizer: Error occurred while launching Sublime Text 3! \n" + result.stderr.decode('utf-8'))
        app.error("Cannot run Sublime Text /// " + str(datetime.now()) + " /// debug analizer: Error occurred while launching Sublime Text 3! /// " + result.stderr.decode('utf-8'))
        # Delete extracted folder in case of error while opening
        if os.path.exists(destination):
            rmtree(destination)
        return 0
    
    app.info("Sublime result : " + str(result))
    app.info("Sublime opened !")


def unZip(path, name):
    print('unzip :' + path + "\nwith name : " + name)

    cmd7z = '"' + sevenZipExecutable + '" x "' + path + '" -bsp1 -y -o' + destination

    app.info("unzipping...")
    # Lazy way of doing the progress bar
    for x in range(1, 9):
        app.setMeter("progress", x*random.randint(1, 10))

    result = subprocess.run(cmd7z, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        print(cmd7z, 'succ -> ' + result.stdout.decode('utf-8'), 'err -> ' + result.stderr.decode('utf-8'))
        app.errorBox("Cannot extract file", str(datetime.now()) + " debug analizer: Error occurred while extracting file \n" + result.stderr.decode('utf-8') + "\nPlease check if the file is corrupted and try again.")
        app.error("Cannot extract file" + " /// debug analizer: Error occurred while extracting file /// " + result.stderr.decode('utf-8') + " /// Please check if the file is corrupted and try again.")
        app.error(cmd7z + ' / succ -> ' + result.stdout.decode('utf-8') + ' / err -> ' + result.stderr.decode('utf-8'))
        app.setMeter("progress", 0)
        return 0
    app.setMeter("progress", 100)

    app.info("7zip result: " + str(result))
    app.info("finished unzipping well !")



# Events
def btnPress(btn):
    global path
    global name
    if btn == 'X':
        clearFileInput()
    else:
        name = app.getEntry("fileName")
        # if there is a space in the name it will be reformatted to the text without spaces
        # and with mayus for each word
        flag = name.split(" ")
        if len(flag) > 1:
            reformat = ''
            for e in flag:
                reformat += str(e).capitalize()
            name = reformat
            #print(name) 
                  
        path = app.getEntry("file")
        

    if btn == 'vscode':
        check(btn)

    if btn == 'sublime':
        check(btn)
    
    if btn == 'Help':
        subprocess.run('START "" https://github.com/joeperpetua/debug-extractor#debug-extractor-docs', shell=True)

    if btn == 'Report Bug':
        subprocess.run('START "" https://github.com/joeperpetua/debug-extractor#bug-report', shell=True)
    
    if btn == 'Close':
        app.hideAllSubWindows()
    

    if btn == 'Download Visual Studio Code':
        subprocess.run('START "" https://code.visualstudio.com/download', shell=True)
    
    if btn == ' Download Visual Studio Code ':
        subprocess.run('START "" https://code.visualstudio.com/download', shell=True)

    if btn == 'Download Sublime Text 3':
        subprocess.run('START "" https://www.sublimetext.com/3', shell=True)

    if btn == 'Download 7zip':
        subprocess.run('START "" https://www.7-zip.org/download.html', shell=True)

    if btn == 'How to add custom entry':
        subprocess.run('START "" https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/', shell=True)


def check(btn):
    global destination
    global name
    global path
    global supported
    global sevenZipExecutable
    global codeExecutable
    global sublimeExecutable

    app.info("--------- start check, globals initialized correctly --------")
    # print('--------------------------------------------------------------------------------------------------------- ', path)
    # Check path possible scenarios
    if path == '':
        print('please select a file')
        app.warningBox("No file selected", "Please select a file to analyze", parent=None)
        app.info("No file selected /// Please select a file to analyze")
        return 0
    elif os.path.exists(path):
        app.info("provided path exists...")
        for element in supportedFiles:
            if path.endswith(element):
                supported = True
                app.info('file type supported: ' + element)

            # print('file is supported: ' + str(supported))
        if not supported:
            app.errorBox("File not supported", "The tool supports only 'dat', 'zip', 'rar', 'tar', '7z', 'gzip' file extensions...\nCheck it")
            app.warn("File not supported /// The tool supports only 'dat', 'zip', 'rar', 'tar', '7z', 'gzip' file extensions...")
            return 0

    # format file name to remove spaces and dots
    tempPath = path.split('/')
    tempPath = tempPath[len(tempPath)-1]
    if ' ' in tempPath:
        tempPath = tempPath.replace(' ', '')
        
    if '.' in tempPath:
        occurences = tempPath.count('.')
        tempPath = tempPath.replace('.', '', occurences - 1)

    # now rename file with formatted name
    os.rename(path,tempPath)

    path = tempPath

    # C:\tickets\name\
    destination += name + bar
    

    # Check directory name possible scenarios
    if name == '':
        print('name not set, ticket will be saved with default name')
        print(path)

        # gives the original file name
        name = path.split("/").pop().split(".")[0]
        destination = "C:" + bar + "tickets" + bar + name + bar

        if os.path.exists(destination):
            name += "_" + str(random.randint(0, 999999))
            destination = "C:" + bar + "tickets" + bar + name + bar


        print(name)
        print(destination)

        
        # name = 'default_' + str(random.randint(0, 999999))
        # Fix crash when no name provided
        
        
        app.info("destination: " + destination)
        
    elif os.path.exists(destination):
        print('Ticket already exists')
        ticketExist = app.questionBox("Existing ticket", "Ticket already exists, do you want to create a subfolder under the existing one to have the two versions?\nIf not, it will be overwritten.", parent=None)
        app.warn("Existing File, running double ticket process")
        # Returns True if create a subfolder, False if overwrite
        if ticketExist:
            if os.path.exists(destination + name + "v2"):
                app.warningBox("Existing ticket", "Cannot have more than 2 version, please delete the newer version or change its directory name.", parent=None)
                app.error("More than two versions already, cannot make a third /// return 0")
                return 0
        
            print("Create subfolder")
            name += "v2"
            # C:\tickets\name\namev2\
            destination += name + bar
            os.mkdir(destination)
            app.info("created destination dir: " + destination)
            
        else:
            print("Overwrite")
            app.info("overwrite selected, deleting destination: " + destination)
            rmtree(destination)
            app.info("GOOD destination deleted !")
        

    # Check if programs are installed

    #7z64 \\ C:\Program Files\7-Zip\7z.exe
    #7z86 \\ C:\Program Files (x86)\7-Zip\7z.exe
    if conf['custom_path']['sevenZip'] != 'path' and os.path.exists(conf['custom_path']['sevenZip']):
        print('custom 7z found')
        sevenZipExecutable = conf['custom_path']['sevenZip']
        app.info('custom 7z found')
    elif os.path.exists(config.path['x64']['sevenZip']):
        print('x64 7z found')
        sevenZipExecutable = config.path['x64']['sevenZip']
        app.info('x64 7z found')
    elif os.path.exists(config.path['x86']['sevenZip']):
        print('x86 7z found')
        sevenZipExecutable = config.path['x86']['sevenZip']
        app.info('x86 7z found')
    else:
        print('7z64 not found')
        launchSubWindow('7zip not found')
        app.error('7z not found')
        return 0

    canRun = 0

    #VScode64 \\ C:Users\USER\AppData\Local\Programs\Microsoft VS Code
    if conf['custom_path']['VScode'] != 'path' and os.path.exists(conf['custom_path']['VScode']):
        print('custom VScode found')
        codeExecutable = conf['custom_path']['VScode']
        canRun += 1
        app.info('custom VScode found')
    elif os.path.exists(config.path['x64']['VScode']):
        print('x64 VScode found')
        codeExecutable = config.path['x64']['VScode']
        canRun += 1
        app.info('x64 VScode found')
    elif os.path.exists(config.path['x86']['VScode']):
        print('x86 VScode found')
        codeExecutable = config.path['x86']['VScode']
        canRun += 1
        app.info('x86 VScode found')
    else:
        print('VScode not found')
        app.warn('VScode not found')


    #Sublime64 \\ C:\Program Files\Sublime Text 3\subl.exe
    #Sublime86 \\ C:\Program Files (x86)\Sublime Text 3\subl.exe 
    if conf['custom_path']['SUB'] != 'path' and os.path.exists(conf['custom_path']['SUB']):
        print('Custom Sublime Text 3 found')
        sublimeExecutable = conf['custom_path']['SUB']
        canRun += 1
        app.info('Custom Sublime Text 3 found')
    elif os.path.exists(config.path['x64']['SUB']):
        print('x64 Sublime Text 3 found')
        sublimeExecutable = config.path['x64']['SUB']
        canRun += 1
        app.info('x64 Sublime Text 3 found')
    elif os.path.exists(config.path['x86']['SUB']):
        print('x86 Sublime Text 3 found')
        sublimeExecutable = config.path['x86']['SUB']
        canRun += 1
        app.info('x86 Sublime Text 3 found')
    else:
        print('Sublime Text 3 not found')
        app.warn('Sublime Text 3 not found')
        

    # Verify flag
    if canRun < 1:
        launchSubWindow('Text editor not found')
        app.err('Text editor not found')
        return 0


    if unZip(path, name) == 0:
        app.error('unzip error')
        return 0
        
    if btn == 'vscode':
        openWithVS(path, name)

    if btn == 'sublime':
        openWithSub(path, name)  
    
    if app.getRadioButton("debug") == "Move .dat file to extracted folder":
        print("moveDebug")
        app.info('moving debug file to destination...')
        os.replace(path, destination  + name + ".dat")
        app.info('debug file moved OK')


    if app.getRadioButton("debug") == "Delete .dat file after extracting it\n(the extracted directory will remain)":
        print("delDebug")
        app.info('deleting debug file...')
        os.remove(path)
        app.info('debug file deleted OK')
    
    if app.getCheckBox("openDebug"):
        app.info('try open VPN debug analyzer...')
        subprocess.run('START "" https://login.vpnsupport.synology.me:4444/webportal.cgi?go=http://192.168.40.40:80/debug/', shell=True)
        app.info('VPN debug analyzer OK')



    destination = "C:" + bar + "tickets" + bar
    path = ''
    supported = False

    app.info("------------------ finished GOOD ------------------")

# Render GUI
if app:
    app.addMenuList("Settings", ["Change settings"], openSettings)
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
    app.addMenuEdit(inMenuBar=False)
    #app.setEntryTooltip("fileName", "If no name is provided a random name will be assigned")
    # File input
    app.addLabel("file label", "Select debug file", row=1, column=0, colspan=2)
    app.setPadding([5,5])
    app.addFileEntry("file", row=1, column=3, colspan=1)
    app.addButton("X", btnPress, row=1, column=4)
    app.setButtonBg("X", "#e5806c")
    app.setButtonRelief("X", "flat")
    app.setButtonCursor("X", "hand2")
    app.setPadding([0,0])
    app.stopFrame()

    app.startFrame('choice')
    app.setFg('grey', override=False)
    app.setSticky("w")

    app.addRadioButton("debug", "Move .dat file to extracted folder")
    app.addRadioButton("debug", "Delete .dat file after extracting it\n(the extracted directory will remain)")
    app.setRadioButtonCursor("debug", "hand2")
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
    app.setButtonCursor("vscode", "hand2")

    app.setButtonImage("sublime", "img/sublime.gif")
    app.setButtonBg("sublime", "#192227")
    app.setButtonRelief("sublime", "flat")
    app.setButtonCursor("sublime", "hand2")
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
    app.setButtonCursor("Help", "hand2")
    app.setSticky("ew")
    app.addImage("logo", "img/logo.gif", row=0, column=1, colspan=2, rowspan=1)
    app.setSticky("e")
    app.addButton("Report Bug", btnPress, row=0, column=3, colspan=1)
    app.setButtonBg("Report Bug", "#4a4e50")
    app.setButtonFg("Report Bug", "#ffffff")
    app.setButtonRelief("Report Bug", "flat")
    app.setButtonCursor("Report Bug", "hand2")
    app.stopFrame()

    # --------------
    # SUBWINDOWS
    # --------------

    app.startSubWindow('7zip not found', modal=True)
    app.setBg('#263238', override=False, tint=False)
    app.setPadding([60,60])

    app.startFrame('modal 7z', row=0, column=0)
    app.addLabel("7zip not found message", "The program 7zip was not found in your system, this is a required\nprogram to run the tool, please install it and try launching the tool again.\n\nYou can also set a custom path in case you have installed the programs in another path than the default one.", row=0, column=0)
    app.stopFrame()

    app.startFrame('modal 7z2', row=1, column=0)
    app.setPadding([60,10])
    app.addButton('Download 7zip', btnPress, row=0, column=0)
    app.addButton(' Set custom path ', openSettings, row=0, column=1)

    app.setButtonBg("Download 7zip", "#4a4e50")
    app.setButtonFg("Download 7zip", "#ffffff")
    app.setButtonRelief("Download 7zip", "flat")
    app.setButtonCursor("Download 7zip", "hand2")

    app.setButtonBg(" Set custom path ", "#4a4e50")
    app.setButtonFg(" Set custom path ", "#ffffff")
    app.setButtonRelief(" Set custom path ", "flat")
    app.setButtonCursor(" Set custom path ", "hand2")

    app.stopFrame()

    app.stopSubWindow()


    app.startSubWindow('Text editor not found', modal=True)
    app.setBg('#263238', override=False, tint=False)
    app.setPadding([60,60])

    app.startFrame('modal te', row=0, column=0)
    app.addLabel("Lb not found message", "The tool could not find nor Visual Studio Code nor Sublime Text 3,\nat least one of them is required to run the tool,\nplease install either of them and try launching the tool again.\n\nYou can also set a custom path in case you have installed the programs in another path than the default one.", row=0, column=0)
    app.stopFrame()

    app.startFrame('modal te2', row=1, column=0)
    app.setPadding([60,10])
    app.addButton('Download Visual Studio Code', btnPress, row=0, column=0)
    app.addButton('Download Sublime Text 3', btnPress, row=0, column=1)
    app.addButton('Set custom path', openSettings, row=0, column=2)

    app.setButtonBg("Download Visual Studio Code", "#4a4e50")
    app.setButtonFg("Download Visual Studio Code", "#ffffff")
    app.setButtonRelief("Download Visual Studio Code", "flat")
    app.setButtonCursor("Download Visual Studio Code", "hand2")

    app.setButtonBg("Download Sublime Text 3", "#4a4e50")
    app.setButtonFg("Download Sublime Text 3", "#ffffff")
    app.setButtonRelief("Download Sublime Text 3", "flat")
    app.setButtonCursor("Download Sublime Text 3", "hand2")

    app.setButtonBg("Set custom path", "#4a4e50")
    app.setButtonFg("Set custom path", "#ffffff")
    app.setButtonRelief("Set custom path", "flat")
    app.setButtonCursor("Set custom path", "hand2")
    app.stopFrame()

    app.stopSubWindow()



    app.startSubWindow('ENV variable for VS Code not found', modal=True)
    app.setBg('#263238', override=False, tint=False)
    app.setPadding([60,60])

    app.startFrame('modal env path message', row=0, column=0)
    app.addLabel("env path not found message", "VS Code entry not found in environment variable PATH. \nThe tool requires it to launch VS code, please install VS Code correctly\nYou can also add it manually from the Control Panel.\n\nYou can click below to download VS Code and install it from scratch or see a guide on \nhow to add a custom entry into the environment variable PATH.\nThe entry has to be on the USER PATH variable and \nhas to point to the /bin directory of VS Code.", row=0, column=0)
    app.stopFrame()

    app.startFrame('modal env path', row=1, column=0)
    app.setPadding([60,10])
    app.addButton(' Download Visual Studio Code ', btnPress, row=0, column=0)
    app.addButton('How to add custom entry', btnPress, row=0, column=1)
    
    app.setButtonBg(" Download Visual Studio Code ", "#4a4e50")
    app.setButtonFg(" Download Visual Studio Code ", "#ffffff")
    app.setButtonRelief(" Download Visual Studio Code ", "flat")
    app.setButtonCursor(" Download Visual Studio Code ", "hand2")

    app.setButtonBg("How to add custom entry", "#4a4e50")
    app.setButtonFg("How to add custom entry", "#ffffff")
    app.setButtonRelief("How to add custom entry", "flat")
    app.setButtonCursor("How to add custom entry", "hand2")
    app.stopFrame()

    app.stopSubWindow()

    # start the GUI
    app.go()
