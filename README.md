# source-rasp

Source code for the foosball embedded Raspberry PI. It runs the UI and manages games.
The UI is done with PyQt5.

## Dependencies
* PyQt5
* pyserial
* autopy
* qtmultimedia5-examples

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

### Replays
Replays are 5-10 seconds clips played when a goal is scored. Those are stored in the parent's `content` directory under the name `replay0.mp4` and `replay1.mp4`.
For the time being, those are provided by the PI camera module.

### DB


## Todo
* [ ] Add the possibility to stop the replay mid-video by pushing any button


# Mac OS X set up

## Requirements (for Mac)
- macOS 10.13 or higher (otherwise Pyqt5 will not work)
- [Homebrew](https://brew.sh/index_fr) installed
- Python 3.5 (or >): `brew install python3` should do it
- `pip` installed (the previous command should have done it too)
- Finally, `virutalenv` installed: `pip install virtualenv`

## Set up the working environment

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

The project can now be run:
```
./devtools.sh exec
```
