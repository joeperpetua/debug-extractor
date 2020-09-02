# import the library
from appJar import gui
# create a GUI variable called app
app = gui("Debug Analyzer", "600x300")
path = ''

def btnPress(btn):
    if btn == 'X':
        clearFileInput()
    else:
        path = app.getEntry("file")

    if btn == 'Open with Visual Studio':
        openWithVS(path)

    if btn == 'Open with Sublime Text':
        openWithSub(path)

def clearFileInput():
    print('clear file')  
    app.clearEntry("file")

def unZip(path):
    print('unzip :' + path)    

def openWithVS(path):
    print('vs :' + path)      

def openWithSub(path):
    print('sub :' + path)      


# Render GUI
if app:
    #app.setSticky("news")
    #app.setExpand("both")
    app.setStretch("both")
    app.setFont(14)

    app.startFrame("header", row=0, column=0)
    app.addLabel("l1", " ", row=0, column=0, colspan=1, rowspan=1)
    app.addLabel("l2", "Select a .dat debug file to open with VScode or Sublime Text 3", row=0, column=1, colspan=1, rowspan=1)
    app.addLabel("l4", " ", row=0, column=2, colspan=1, rowspan=1)
    app.stopFrame()

    app.setPadding([60,10])
    app.startFrame("body", row=1, column=0, colspan=4, rowspan=2)
    app.setPadding([0,0])

    # File name input
    app.addLabel("name label", "Custom name\nfor the file", row=0, column=0, colspan=2)
    app.addEntry("fileName", row=0, column=3)
    # File input
    app.addLabel("file label", "Select debug file", row=1, column=0, colspan=2)
    app.setPadding([5,5])
    app.addFileEntry("file", row=1, column=3, colspan=1)
    app.addButton("X", btnPress, row=1, column=4)
    app.setPadding([0,0])
    app.stopFrame()


    app.startFrame("footer", row=3, column=0)
    app.addButtons(["Open with Visual Studio", "Open with Sublime Text"], btnPress,row=0, column=0,)
    app.setPadding([60,40])
    app.addImage("logo", "logo.gif", row=1, column=0, colspan=2, rowspan=1)
    app.stopFrame()


    # start the GUI
    app.go()
