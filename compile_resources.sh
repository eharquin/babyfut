#! /bin/sh

# Modules
pyuic5 --import-from=ui ui/main.ui        -o ui/main_ui.py
pyuic5 --import-from=ui ui/menu.ui        -o ui/menu_ui.py
pyuic5 --import-from=ui ui/game.ui        -o ui/game_ui.py
pyuic5 --import-from=ui ui/endgame.ui     -o ui/endgame_ui.py
pyuic5 --import-from=ui ui/options.ui     -o ui/options_ui.py
pyuic5 --import-from=ui ui/authquick.ui   -o ui/authquick_ui.py
pyuic5 --import-from=ui ui/leaderboard.ui -o ui/leaderboard_ui.py

# Custom widgets
pyuic5 --import-from=ui ui/playerlist.ui -o ui/playerlist_ui.py

pyrcc5 -root /ui        ui/assets.qrc     -o ui/assets_rc.py
