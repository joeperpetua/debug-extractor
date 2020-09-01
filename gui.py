# import the library
from appJar import gui
# create a GUI variable called app
app = gui("Debug Analyzer", "600x400")

#app.setSticky("news")
#app.setExpand("both")
app.setFont(14)

def btnPress(btn):
    pass

#Helper -- label args = name, text to render, row, col, colspan, rowspan
app.startFrame("header", row=0, column=0)
#Row 0
app.addLabel("l1", " ", 0, 0, 1, 1)
app.addLabel("l2", "Select a .dat debug file to open with VScode or Sublime Text 3", 0, 1, 1, 1)
app.addLabel("l4", " ", 0, 2, 1, 1)
app.stopFrame()

app.startFrame("body", row=1, column=0, colspan=3, rowspan=2)
#Row 1
app.addLabel("l5", "", 1, 0, 1, )
app.addButton("Select file", btnPress, 1, 1, 1, 3)
app.addLabel("l8", "", 1, 2, 1, 3)
app.stopFrame()
#Row 2 and 3 get rendered empy and then they get overwritten by Row 1

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