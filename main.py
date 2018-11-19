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

from PyQt5 import QtWidgets

def getContent(path):
	contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
	return join(contentFolder, path)
	
if __name__=='__main__':
	from ui.mainwin import MainWin
	from modules import GameModule
	from player import Side
	
	from input import GPIOThread
	from database import Database
	from replay import Replay as ReplayThread
	
	try:
		#logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
		logging.basicConfig(level=logging.DEBUG)
		
		app = QtWidgets.QApplication(sys.argv)
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
