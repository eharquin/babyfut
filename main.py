#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sys
import logging
import threading
from os.path import dirname, abspath, join

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsBlurEffect, QApplication
from PyQt5.QtCore import QTime, Qt

from ui.main_ui import Ui_MainWindow
from modules import *
from player import Side
from com import InputThread

class MainWin(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		#Background blur
		bgBlur = QGraphicsBlurEffect()
		bgBlur.setBlurHints(QGraphicsBlurEffect.QualityHint)
		#bgBlur.setBlurRadius(5)
		#self.ui.panels.setGraphicsEffect(bgBlur)
		
		# Module loading
		self.modules = [
			MenuModule(self),
			AuthQuickModule(self),
			AuthLeagueModule(self),
			GameModule(self),
			EndGameModule(self),
			LeaderboardModule(self),
			OptionsModule(self)
		]
		
		for mod in self.modules:
			self.ui.panels.addWidget(mod)
		
		self.ui.panels.setCurrentIndex(0)
		self.ui.panels.currentWidget().setFocus()
		self.ui.panels.currentWidget().grabKeyboard()
		self.ui.panels.currentWidget().load()
		self.displaySystemTime()
		self.startTimer(1000)
	
	#def eventFilter(target, event):
	#	return event.type()==QEvent.KeyPress and event.key() not in acceptedKeys

	def timerEvent(self, e):
		self.displaySystemTime()

	def displaySystemTime(self):
		self.ui.lcdTime.display(QTime.currentTime().toString("hh:mm:ss"))

	def findMod(self, type):
		mod_idx = [i for i, x in enumerate(self.modules) if isinstance(x, type)]
		return -1 if len(mod_idx)==0 else mod_idx[0]
	
	def dispatchMessage(self, msg, toAll=False):
		modulesIdx = self.modules if toAll else [self.findMod(type(self.ui.panels.currentWidget()))]			
		for modIdx in modulesIdx:
			self.modules[modIdx].other(**msg)
	
	@staticmethod
	def getContent(path):
		contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
		return join(contentFolder, path)

	def _refreshAfterSettings(self):
		from settings import Settings
		
		if Settings.ui['fullscreen']:
			self.showFullScreen()
			QApplication.setOverrideCursor(Qt.BlankCursor);
		else:
			self.showNormal()
			QApplication.setOverrideCursor(Qt.ArrowCursor);

if __name__=='__main__':
	from settings import Settings
	
	#logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
	logging.basicConfig(level=logging.DEBUG)
	
	app = QtWidgets.QApplication(sys.argv)
	myapp = MainWin()
	
	if Settings['app.mode']!='dev':
		threadArduinoLeft  = InputThread(myapp, Side.Left)
		#threadArduinoRight = InputThread(myapp, Side.Right)
		threadArduinoLeft.start()
		#threadArduinoRight.start()
	
	myapp.show()
	app.exec_()
	
	if Settings['app.mode']!='dev':
		threadArduinoLeft.stop()
		#threadArduinoRight.stop()
		threadArduinoLeft.join()
		#threadArduinoRight.join()
