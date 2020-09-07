# Debug Analyzer Docs

Description

## Requirements
- [7zip](https://www.7-zip.org/download.html)
- At least one of the following:
  - [Visual Studio Code](https://code.visualstudio.com/download)
  - [Sublime Text 3](https://www.sublimetext.com/3)
  
## Setup

### Visual Studio Code
Visual Studio Code extensions and configurations for better log reading:
- Setup:
  - In user setting .json file add this lines to support all the different files the debug.dat file contains:
  ```markdown
  "files.associations": {
    "*.log.*": "log",
    "messages": "log",
    "*.error.*": "log"
  },
  ```
- Extensions:
  - [Log File Highlighter](https://marketplace.visualstudio.com/items?itemName=emilast.LogFileHighlighter&ssr=false#overview)
    
### Sublime Text 3
Sublime Text 3 extensions and configurations for better log reading:
- Setup:
  - Setup 1
  - Setup 2
  - In Sublime Text preferences file add this lines to avoid openning 2 windows each time a debug file is open:
    ```markdown
    "hot_exit": false,
    "remember_open_files": false
    ```


## Bug Report
@chat joelperpetua or gianpieromarcotullio
