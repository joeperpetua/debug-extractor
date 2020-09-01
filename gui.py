# import the library
from appJar import gui
# create a GUI variable called app
app = gui("Debug Analyzer", "600x300")

#app.setSticky("news")
#app.setExpand("both")
app.setStretch("column")
app.setFont(14)

def btnPress(btn):
    pass


app.startFrame("header", row=0, column=0)

app.addLabel("l1", " ", row=0, column=0, colspan=1, rowspan=1)
app.addLabel("l2", "Select a .dat debug file to open with VScode or Sublime Text 3", row=0, column=1, colspan=1, rowspan=1)
app.addLabel("l4", " ", row=0, column=2, colspan=1, rowspan=1)
app.stopFrame()

app.startFrame("body", row=1, column=0, colspan=3, rowspan=2)
app.setPadding([60,0])
app.addEntry("fileName", row=0, column=0, )
app.addFileEntry("file", row=1, column=0)
app.startLabelFrame("", 0, 0)
app.addImage("logo", "logo.png")
app.stopLabelFrame()
app.setPadding([0,0])
app.stopFrame()


app.startFrame("footer", row=3, column=0)
app.addButtons(["Open with Visual Studio", "Open with Sublime Text"], btnPress,row=0, column=0,)
app.stopFrame()




# #Row 2
# app.addLabel("l9", "", 2, 0, 3)

# #Row 3
# app.addLabel("l10", "", 3, 0, 3)






# app.setLabelBg("l2", "grey")
# app.setLabelBg("l1", "black")
# app.setLabelBg("l4", "black")
# app.setLabelBg("l6", "green")


# start the GUI
app.go()