# source-rasp

Source code for the foosball embedded Raspberry PI. It runs the UI and manages games.
The UI is done with PyQt5.

## Launch
* Make sure to have Python>3.5 installed (`sudo apt-get install python3` otherwise)
* Make sure to have PyQt5 installed (`sudo pip install pyqt5` otherwise)
* Compile the .ui and .rc files: `./compile_resources.sh`
* Execute main.py: `python3 main.py`

## Edit the UI
The UI is mostly created using Qt-Designer:
* Download qt4-designer (`sudo apt-get install qt4-designer`)
* Edit .ui files with qt4-designer
* Compile the .ui in a python file: `./compile_resources.sh`
* Done!

## Sofware Organisation
### UI
The UI is only made of one window with static widgets and changing "modules".
There are currently 3 modules:
* Main menu, showed on startup and giving access to other panels
* Game, containing the scores, timers, etc of the current game
* Options, to allow the user tp configure some options
* Authentification for two players
* ...

Those inherit from the `Module` class and are composed of 5 things:
* Access to the main window, through the `parent_win` member
* A widget (built from a .ui file, see sections above)
* 3 management functions:
  * Load: run every time the module is showed, meant to start timers & co
  * Unload: run every time the module is hidden, meant to stop timers & co
  * Other: can be called at any time by other modules, meant to exchange informations

The widget contained by each module are stacked in a QStackedWidget and only one of them can be seen at a time.
To get from one to the other, the current module is unloaded current, then the new one is shown and loaded.
Each module can overload the load/unload/other method in order to have a specific behavior.

### DB


## Todo
* [ ] ...
