#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
modifications : Laurine Dictus, Anaël Lacour
"""

import os
from os.path import dirname, abspath, join, exists
import glob
import sys
import logging

from PyQt5 import QtCore
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

ON_RASP = os.uname()[1] == 'raspberrypi'
IMG_PATH = getContent('img')

if __name__=='__main__':
	__package__ = 'Babyfut'
	from Babyfut.ui.mainwin import MainWin
	from Babyfut.modules import GameModule
	from Babyfut.core.player import Side
	from Babyfut.core.input import Input
	from Babyfut.core.downloader import Downloader
	from Babyfut.core.database import Database
	from Babyfut.core.replay import Replay as ReplayThread
	from Babyfut.core.server import Server

	try:
		#logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
		logging.basicConfig(level=logging.DEBUG)

		app = QApplication(sys.argv)
		myapp = MainWin()

		if not exists(IMG_PATH):
			 os.makedirs(IMG_PATH)

		if ReplayThread.isCamAvailable():
			threadReplay = ReplayThread(Side.Left)
			threadReplay.start()
			myapp.dispatchMessage({'replayThread': threadReplay}, toType=GameModule)

		input = Input()
		input.rfidReceived.connect(lambda side, rfid: myapp.dispatchMessage({'rfid': rfid, 'source': side}))
		input.goalDetected.connect(lambda side      : myapp.dispatchMessage({'goal': True, 'source': side}))
		input.start()

		server = Server()
		server.start()
		threadDownloader = Downloader.instance()
		threadDownloader.start()

		myapp.show()
		app.exec_()


		if ReplayThread.isCamAvailable():
			threadReplay.stop()
			threadReplay.join()

		input.stop()
		server.closeConn()
		server.stop()
		server.join()
		threadDownloader.stop()
		threadDownloader.join()

	finally:
		Database.instance().close()
		for f in glob.glob(join(IMG_PATH, '*')):
			os.remove(f)
