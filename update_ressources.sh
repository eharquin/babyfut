#! /bin/sh

pyuic5 main.ui -o main_ui.py
pyuic5 menu.ui -o menu_ui.py
pyuic5 game.ui -o game_ui.py
pyuic5 options.ui -o options_ui.py
pyrcc5 assets.qrc -o assets_rc.py
