import os

path = dict(
    x86 = dict(
        sevenZip = "C:/Program Files (x86)/7-Zip/7z.exe",
        VScode = "C:/Users/" + os.getlogin() + "/AppData/Local/Programs/Microsoft VS Code",
        SUB = "C:/Program Files (x86)/Sublime Text 3/subl.exe",
    ),
    x64 = dict(
        sevenZip = "C:/Program Files/7-Zip/7z.exe",
        VScode = "C:/Users/" + os.getlogin() + "/AppData/Local/Programs/Microsoft VS Code",
        SUB = "C:/Program Files/Sublime Text 3/subl.exe",
    )
)

