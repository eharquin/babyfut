# source-rasp

Source code for the foosball embedded Raspberry PI. It runs the UI and manages games.

The UI is done with PyQt.

## Edit the UI
* Download qt4-designer (`sudo apt-get install qt4-designer`)
* Edit .ui files with qt4-designer
* Convert the .ui files to python sources (`pyuic5 file.ui -o file_ui.py`)
* Done!

## UI Organisation
The software is composed of only one window in which "panels" change. There are currently 3 panels:
* The main menu, default panel shown on startup
* The game itself, containing the scores, timers, ...
* The options menu, to configure some options

Those panels are stacked (in a QStackedWidget) and only one of them can be shown at a time.
We can then "swap" from one to the other, making sure to unload the previous and to load the )
For better control over what is being run, panels can be unloaded when swapped and re-loaded when shown again.
This can be done through two overloadable functions: load and unload.
Each panel (inheriting from the Panel class) can use those to perform actions when shown or hidden