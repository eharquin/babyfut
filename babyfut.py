#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
OnRasp = os.uname()[1] == 'raspberrypi'

import sys
import logging
from os.path import dirname, abspath, join

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication

def getContent(path):
	contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
	return join(contentFolder, path)

def getMainWin():
	from Babyfut.ui.mainwin import MainWin

	# Global function to find the (open) QMainWindow in application
	for widget in QApplication.instance().topLevelWidgets():
		if isinstance(widget, QMainWindow):
			return widget
	return None

if __name__=='__main__':
	print(__package__)
	from Babyfut.ui.mainwin import MainWin
	from Babyfut.modules import GameModule
	from Babyfut.core.player import Side
	from Babyfut.core.settings import Settings
	from Babyfut.core.input import GPIOThread
	from Babyfut.core.database import Database
	from Babyfut.core.replay import Replay as ReplayThread

	try:
		#logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
		logging.basicConfig(level=logging.DEBUG)

		app = QtWidgets.QApplication(sys.argv)
		lang = Settings['ui.language']
		qtTranslator = QtCore.QTranslator()
		if lang!='en' and qtTranslator.load("translations/babyfut_{}.qm".format(lang)):
			app.installTranslator(qtTranslator)

		myapp = MainWin()

		if ReplayThread.isCamAvailable():
			threadReplay = ReplayThread(Side.Left)
			threadReplay.start()
			myapp.dispatchMessage({'replayThread': threadReplay}, toType=GameModule)

		threadGPIO = GPIOThread(myapp)
		threadGPIO.start()

		myapp.show()
		app.exec_()

		threadGPIO.stop()

		if ReplayThread.isCamAvailable():
			threadReplay.stop()
			threadReplay.join()

		threadGPIO.join()

	finally:
		GPIOThread.clean()
		Database.instance().close()
