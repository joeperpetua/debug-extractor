# import the library
from appJar import gui
# create a GUI variable called app
app = gui("Debug Analyzer", "600x300")

#app.setSticky("news")
#app.setExpand("both")
app.setStretch("column")
app.setFont(14)

def btnPress(btn):
    print(app.getEntry("file"))


app.startFrame("header", row=0, column=0)

app.addLabel("l1", " ", row=0, column=0, colspan=1, rowspan=1)
app.addLabel("l2", "Select a .dat debug file to open with VScode or Sublime Text 3", row=0, column=1, colspan=1, rowspan=1)
app.addLabel("l4", " ", row=0, column=2, colspan=1, rowspan=1)
app.stopFrame()

app.startFrame("body", row=1, column=0, colspan=3, rowspan=2)
app.setPadding([60,10])
app.setStretch("both")
# File name input
app.addLabel("name label", "Custom name for the file", row=0, column=0, colspan=2)
app.setStretch("column")
app.addEntry("fileName", row=0, column=3)
# File input
app.addLabel("file label", "Select debug file", row=1, column=0, colspan=2)
app.addFileEntry("file", row=1, column=3)

#app.addImage("logo", "logo.png", row=2, column=0)

app.setPadding([0,0])
app.stopFrame()


app.startFrame("footer", row=3, column=0)
app.addButtons(["Open with Visual Studio", "Open with Sublime Text"], btnPress,row=0, column=0,)
app.stopFrame()


# start the GUI
app.go()