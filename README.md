# source-rasp

Source code for the football embedded Raspberry PI.
It runs the UI and manages games.
The UI is done with PyQt5.

Mac OS X set up below

## Dependencies
* PyQt5
* pyautogui
* qtmultimedia5-examples

## Launch
* Make sure to have Python>3.5 installed (`sudo apt-get install python3` otherwise)
* Make sure to have PyQt5 installed (`sudo pip install pyqt5` otherwise)
* Compile the .ui and .rc files: `./devtools.sh ui`
* Execute the software: `./devtools.sh exec`

## Edit the UI
The UI is mostly created using Qt-Designer:
* Download qt4-designer (`sudo apt-get install qt4-designer`)
* Edit .ui files with qt4-designer
* Compile the .ui in a python file: `./devtool.sh ui`
* Done!

## Sofware Organisation
### UI
The UI is only made of one window with static widgets and changing "modules".
There are currently 7 modules:
* Main menu, showed on startup and giving access to other panels
* Game, containing the scores, timers, etc of the current game
* Leaderboard, for comparing players scores, times, etc + delete itself from the database
* Options, to allow the user to configure some options(language, max score, etc)
* Authentification for 2 to 4 players in party mode
* Authentification for n players in league mode
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

### Threads
In addition to the main UI thread, there are 3 other threads running:
* Input, managing buttons control, rfid reading and goal detection
* Replay, capturing video during a match and storing it when there is a goal
* Server, waiting for messages from the second raspberry PI


### Settings
Settings are stored in a JSON file located in the parent's `content` directory, that looks like:
```
{
    "app": {
		"loglevel": {
			"type": "combo",
			"value": "debug",
			"values": [
				"debug",
				"info",
				"warning",
				"error",
				"critical"
			]
		}
	},
    "ui": {
        "fullscreen": {
            "type": "boolean",
            "value": false
        }
    },
    "picam": {
        "resolution": {
            "type": "combo",
            "value": [640, 480],
            "values": [
                [1920, 1080],
                [1280, 720],
                [640, 480]
            ]
        }
    },
    "replay": {
        "duration": {
            "type": "range",
            "value": 5,
            "range": [1, 10]
        }
    }
}
```

That JSON file is parsed and can be accessed by doing:
```
from settings Import Settings
Settings['ui.fullscreen'] = False
duration = Settings['replay.duration']
```

Note that for potential security reasons, this file is not synchronized with git, but is downloadable on the PR's GDrive

### Replays
Replays are 5-10 seconds clips played when a goal is scored. Those are stored in the parent's `content` directory under the name `Replay Left.mp4` and `Replay Right.mp4`.
Those are provided by the PI camera module, thanks to another thread that records the video while a game takes place and stores it once a goal is marked.

## DB
The database is currently in SQLite but should be transposable to MySQL later on. There are 3 tables:
* Players: Storing player information (name, rfid, etc)
* Matches: Storing matches start/stop times and winners/losers
* Teams: Linking players and matches

## Todo
* [x] Check validity of replays on a real rasp
* [ ] Check validity of rfid on a real rasp
* [ ] League mode
* [ ] Translation on the fly (instead of having to manually restart)
* [x] Installation guide
* [x] Connection to another PI to exchange RFID and videos
* [ ] Integration of the real UTC DB


# Mac OS X set up

## Requirements
- First make sure to have Mac OS X 10.13 or higher on your device. Otherwise Pyqt5 will not work.
- Make sure to have homebrew installed (`https://brew.sh/index_fr` otherwise)
- Create a folder named "pr_baby"
- Clone repositories from Gitlab `git clone https://gitlab.utc.fr/pr_babyfut/pr_baby_app_esclave` and `git clone https://gitlab.utc.fr/pr_babyfut/babyfut`
- Rename babyfut in Babyfut
- In Babyfut folder, create a new folder named content
- Put `babyfut.sqlight`and `settings.json`in the content folder

## Set up a virtualenv

You may find in the previous readme that dependancies troubles may occure. In order not to use a virtual machine you can set a virtualenv.

- `cd Babyfut`
- `virtualenv -p python 3 venv`
- `source venv/bin/activate`
- `pip install pyqt5`

## Compile and launch the app

Once your virtualenv set up done (venv should appear in front of the command line) compile the UI source

- `./devtools.sh ui`

The project can now be run

- `./devtools.sh exec`


