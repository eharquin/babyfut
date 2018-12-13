#! /bin/bash

WD=$(pwd)

cd "$( dirname "${BASH_SOURCE[0]}" )"

case "$1" in
	"ui"|"update_ui"|"build_ui")
		echo "Building UI..."

		echo "	Modules"
		pyuic5 --import-from=Babyfut.ui ui/main.ui        -o ui/main_ui.py
		pyuic5 --import-from=Babyfut.ui ui/menu.ui        -o ui/menu_ui.py
		pyuic5 --import-from=Babyfut.ui ui/game.ui        -o ui/game_ui.py
		pyuic5 --import-from=Babyfut.ui ui/endgame.ui     -o ui/endgame_ui.py
		pyuic5 --import-from=Babyfut.ui ui/options.ui     -o ui/options_ui.py
		pyuic5 --import-from=Babyfut.ui ui/authquick.ui   -o ui/authquick_ui.py
		pyuic5 --import-from=Babyfut.ui ui/authleague.ui  -o ui/authleague_ui.py
		pyuic5 --import-from=Babyfut.ui ui/leaderboard.ui -o ui/leaderboard_ui.py
		pyuic5 --import-from=Babyfut.ui ui/privacy.ui     -o ui/privacy_ui.py

		echo "	Custom Widgets"
		pyuic5 --import-from=Babyfut.ui ui/playerlist.ui     -o ui/playerlist_ui.py
		pyuic5 --import-from=Babyfut.ui ui/delete_dialog.ui  -o ui/delete_dialog_ui.py
		pyuic5 --import-from=Babyfut.ui ui/consent_dialog.ui -o ui/consent_dialog_ui.py

		echo "	Resources"
		pyrcc5 -root /Babyfut/ui        ui/assets.qrc     -o ui/assets_rc.py
		echo "Done."
		;;
	"clean"|"clear")
		echo "Clearing the project..."
		rm -f ui/*_ui.py
		rm -f ui/*_rc.py
		rm -f translations/*.qm

		rm -rf __pycache__
		rm -rf ui/__pycache__
		rm -rf core/__pycache__
		rm -rf modules/__pycache__
		echo "Done."
		;;
	"tru"|"trupdate")
		echo "Updating translation files..."
		pylupdate5 -verbose *.py modules/*.py ui/*.py -ts translations/babyfut_fr.ts
		echo "Done. You can modify generated .ts files with Qt Linguist"
		;;
	"trr"|"trrelease")
		echo "Building translation files..."
		lrelease translations/*
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
	"run"|"exec")
		cd ..
		python -m Babyfut.babyfut
		;;
	*)
		echo "Unknown command \"$1\". See script for available commands."
		;;
esac

cd $WD
