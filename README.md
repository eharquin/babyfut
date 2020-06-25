# source-rasp

Source code for the football embedded Raspberry PI.
It runs the UI and manages games.
The UI is done with PyQt5.

## Requirements
- Python 3.5 (or >): `sudo apt-get install python3` should do it
- `pip` installed (the previous command should have done it too)
- Finally, `virutalenv` installed: `pip install virtualenv`


## Set-up the virtual environment

*You may find in some `readme` files that dependency problems may occure. In order not to use a virtual machine for that, we will set a Python virtual environment.*
```bash
cd pr_babyfut
# the command below creates a virualenv
virtualenv -p python3 venv
# we activate the virtualenv (this should be done
# before each time you will work on the projet)
source venv/bin/activate
pip install -r babyfut/requirements.txt
```

## Compile the UI and launch the app

Once your virtualenv set up is done and activated (`(venv)` should appear in front of the command line) compile the UI source:
```
./devtools.sh ui
```

The project can now be run, for that you need to run 1 master :
```
./devtools.sh master
```
and 2 slaves :

```
./devtools.sh slave
```

## Edit the UI
The UI is mostly created using Qt-Designer:
* Download qt4-designer (`sudo apt-get install qt4-designer`)
* Edit .ui files with qt4-designer
* Compile the .ui in a python file: `./devtool.sh ui`
* Done!


## Sofware Organisation
### UI
The UI is only made of one window with static widgets and changing "modules".
There are currently 11 modules:
* Main menu, showed on startup and giving access to other panels
* Game, containing the scores, timers, etc of the current game
* Leaderboard, for comparing players scores, times, etc + delete itself from the database
* Edit, display player's profile
* Options, to allow the user to configure some options(language, max score, etc)
* Authentification for 2 to 4 players in party mode
* Tournament creation, allow to create a tournament and set up its name
* Tournament registration, allow to add players or teams to a tournament
* Endgame, giving the winner(s) and storing results in the db

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


### Settings
Settings are stored in a JSON file located in the parent's `content` directory.

That JSON file is parsed and can be accessed by doing:
```
from common.settings Import Settings
Settings['ui.fullscreen'] = False
duration = Settings['replay.duration']
```

### Replays
Replays are 5-10 seconds clips played when a goal is scored. Those are stored in the parent's `content` directory..
Those are provided by the PI camera module, thanks to another thread that records the video while a game takes place and stores it once a goal is marked. Replays can be disabled in the `settings` file.

## DB
The database is currently in SQLite. See the doc folder for further information.

## API Ginger


## Todo
* [ ] Continue Tournament mode
* [ ] Get Ginger API key
* [ ] Installation guide for raspberry deployment
* [ ] Declare raspberry's MAC adress on UTC network

