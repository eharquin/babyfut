#! /bin/bash

WD=$(pwd)

cd "$( dirname "${BASH_SOURCE[0]}" )"

case "$1" in
	"ui"|"update_ui"|"build_ui")
		echo "Building UI..."

		echo "	Modules"
		cd ./babyfut_master
		pyuic5 --import-from=. ui/main.ui        -o ui/main_ui.py
		pyuic5 --import-from=. ui/menu.ui        -o ui/menu_ui.py
		pyuic5 --import-from=. ui/game.ui        -o ui/game_ui.py
		pyuic5 --import-from=. ui/endgame.ui     -o ui/endgame_ui.py
		pyuic5 --import-from=. ui/options.ui     -o ui/options_ui.py
		pyuic5 --import-from=. ui/authquick.ui   -o ui/authquick_ui.py
		pyuic5 --import-from=. ui/authleague.ui  -o ui/authleague_ui.py
		pyuic5 --import-from=. ui/leaderboard.ui -o ui/leaderboard_ui.py
		pyuic5 --import-from=. ui/privacy.ui     -o ui/privacy_ui.py
		pyuic5 --import-from=. ui/edit.ui     	 -o ui/edit_ui.py

		echo "	Custom Widgets"
		pyuic5 --import-from=. ui/playerlist.ui     -o ui/playerlist_ui.py
		pyuic5 --import-from=. ui/delete_dialog.ui  -o ui/delete_dialog_ui.py
		pyuic5 --import-from=. ui/consent_dialog.ui -o ui/consent_dialog_ui.py
		pyuic5 --import-from=. ui/team_name_dialog.ui -o ui/team_name_dialog_ui.py
		pyuic5 --import-from=. ui/gamelist.ui     -o ui/gamelist_ui.py
		pyuic5 --import-from=. ui/teamlist.ui     -o ui/teamlist_ui.py
		pyuic5 --import-from=. ui/create_tournament_dialog.ui     -o ui/create_tournament_dialog_ui.py
		pyuic5 --import-from=. ui/tournamentlist.ui     -o ui/tournamentlist_ui.py
		pyuic5 --import-from=. ui/tournamentparticipant.ui     -o ui/tournamentparticipant_ui.py
		pyuic5 --import-from=. ui/tournamentdisplay.ui     -o ui/tournamentdisplay_ui.py



		echo "	Resources"
		pyrcc5 -root /babyfut_master/ui        ui/assets.qrc     -o ui/assets_rc.py
		cd ..
		echo "Done."
		;;
	"clean"|"clear")
		echo "Clearing the project..."
		rm -f babyfut_master/ui/*_ui.py
		rm -f babyfut_master/ui/*_rc.py
		rm -f babyfut_master/translations/*.qm
		find . -type f -name '*.pyc' -delete
		find . -type d -name '__pycache__' -exec rm -rf {} +

		echo "Done."
		;;
	"tru"|"trupdate")
		echo "Updating translation files..."
		cd ./babyfut_master
		pylupdate5 -verbose *.py modules/*.py ui/*.py -ts translations/babyfut_fr.ts
		cd ..
		echo "Done. You can modify generated .ts files with Qt Linguist"
		;;
	"trr"|"trrelease")
		echo "Building translation files..."
		lrelease babyfut_master/translations/*
		echo "Done."
		;;
	"all"|"build_all")
		bash ./devtools.sh "ui"
		bash ./devtools.sh "tru"
		bash ./devtools.sh "trr"
		;;
	"allc"|"build_all_clean")
		bash ./devtools.sh "clean"
		bash ./devtools.sh "all"
		;;
	"run"|"exec"|"master")
		python3 -m babyfut_master.babyfut_master
		;;
	"slave")
		python3 -m babyfut_slave.babyfut_slave
		;;
	"install")
		echo "Installing.."
		echo "** Assuming debian-like environment. This shouldn't be run more than once"
		echo "** Updating the system to make sure everything is up-to-date."
		echo ""
		sudo apt-get update && sudo apt-get upgrade

		echo ""
		echo "** Installing python3 and python tools"
		# Sometimes the PYTHONPATH wont be set accordingly for some raspbian distributions
		# In which case, manually import the right path (/usr/lib/python3/dist-packages) in
		# the virtual environment's activation script
		sudo apt-get install -y python3 python3-venv python3-pyqt5 python3-pip qtmultimedia5-examples \
			 pyqt5-dev pyqt5-dev-tools

		echo ""
		echo "** Setting up the python virtual environment"
		python3 -m venv ../PyQt5
		source ../PyQt5/bin/activate

		echo ""
		echo "** Installing libraries used by the software"
		pip install pi-rc522 pyautogui Xlib RPi.GPIO request

		echo ""
		echo "****************************"
		echo ""
		echo "Installation done successfully! You may have to source the v-env."
		echo "Don't forget to download the \"content\" folder from another source."
		bash ./devtools.sh "allc"
		;;
	*)
		echo "Unknown command \"$1\". See script for available commands."
		;;
esac

cd $WD
