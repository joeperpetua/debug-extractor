# Debug Extractor Docs

This is a tool developed to extract and open debug files from Synology servers. Read documentation for more information about setup with the text editors and how the tool works. 

## Requirements
- [7zip](https://www.7-zip.org/download.html)
- At least one of the following:
  - [Visual Studio Code](https://code.visualstudio.com/download)
  - [Sublime Text 3](https://www.sublimetext.com/3)

## Limitations
- Visual Studio Code has to be added to PATH environment variable in order to work as per Electron limitations when using the direct executable file. (It should be added by default on VS Code instalation)
- Cannot properly open SRM debug files.
- Cannot change default extraction path (C:\\tickets\\).
- Debug files bigger than 400MB could freeze the program for a few seconds. 
- Name of ticket cannot contain the following: 
  - Spaces ( )
  - Double quotes (")

## The basics
The functioning of this program is very simple: Extract and Open.
<br>
Now you can take advantage of some of the perks you have by using either Visual Studio Code or Sublime Text.
<br><br>
First of all, the logs are stored and organized by name in a custom directory, this is:
- C:\tickets\

You can give them the name you want, this being the ticket number, the description of the ticket, name of the package, etc. (See [Limitations section](#limitations) to know what type of names you can set).
<br><br>
In the case that no name is set, the ticket will be stored as the current name of the debug file. If that name already exists on the tickets folder, a random token will be added at the end of the file name.
Example:
- C:\tickets\debug(1)\ 
- C:\tickets\debug(1)_839461\
- C:\tickets\debug(1)_294607\ 
- ...

<br>

When opening a debug file you have two options:
- Move the original debug file to the extracted directory
- Delete the original debug file

By default the file will not be deleted and it will be stored to the extraction directory. 
<br>
You will also have the option to launch a browser tab/window with the office server debug analyzer tool.
<br><br>
To open the debug, you can choose between Visual Studio Code and Sublime Text 3.
<br>
Both of these text editor provide some usefull shortcuts and functions that allow you to find and manage the logs and keywords you need to work with.
<br>
You can check the next section to take a look at what these text editors provide you.
<br><br>

## Setup

### General set up

To easily access the tool you can pin it on your task bar:
<br>

![Debug Extractor Pin](https://i.imgur.com/aJmkPMN.png)

Remember to not delete the main directory were you have extracted the source .zip file.

<br>

In the case that you have either 7Zip, VS Code or Sublime Text 3 installed in non-default locations, you can set custom paths for them.
<br><br>
To do this you can go to the Settings tab on the top left of the program window:
<br>

![Debug Extractor Settings Tab](https://i.imgur.com/fEQkWvn.png)

<br>

After clicking this tab the config.yml file will open and you will be able to edit set the custom path for the programs you desire:
<br>

![Debug Extractor Settings File](https://i.imgur.com/nnYV3ca.png)

Please follow the instructions stated on the file itself to correctly set the paths for the program you want to use.

<br><br>

### Visual Studio Code
Visual Studio Code extensions and configurations for better log reading:
- Setup:
  - In user setting .json file (File -> Preferences -> Settings -> Open Settings (JSON) on the top right of the screen) add this lines to support all the different files the debug.dat file contains:
  ```markdown
  "files.associations": {
    "*log*": "log",
    "messages": "log",
    "*error*": "log"
  },
  ```
- Extensions:
  - [Log File Highlighter](https://marketplace.visualstudio.com/items?itemName=emilast.LogFileHighlighter&ssr=false#overview)
- Useful shortcuts:
  - __Search keyword in all files:__ Ctrl + Shift + F
  - __Search keyword in opened file:__ Ctrl + F
  - __Search file:__ Ctrl + E __or__ Ctrl + P
    
<br><br>

### Sublime Text 3
Sublime Text 3 extensions and configurations for better log reading:
- Setup:
  - In Sublime Text preferences file add this lines into the settings json file to avoid openning 2 windows each time a debug file is open (add between the brackets):
    ```markdown
    "hot_exit": false,
    "remember_open_files": false
    ```
- Useful shortcuts:
  - __Search keyword in all files:__ Ctrl + Shift + F
  - __Search keyword in opened file:__ Ctrl + F
  - __Search file:__ Ctrl + P


## Bug Report
You can check the daemon.log that is on the source directory of the tool, then contact me @chat (joelperpetua) and send me the daemon.log with a description of the issue.

