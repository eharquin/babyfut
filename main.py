#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sys
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtCore import QTime, Qt

from ui.main_ui import Ui_MainWindow
from modules import *

#acceptedKeys = [Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return, Qt.UpArrow, Qt.DownArrow, Qt.LeftArrow, Qt.RightArrow]

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
		self.modules = [MenuModule, GameModule, OptionsModule, AuthModule, LeaderboardModule]
		
		for mod in self.modules:
			self.ui.panels.addWidget(mod(self))
		
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

if __name__=='__main__':
	app = QtWidgets.QApplication(sys.argv)
	#logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
	logging.basicConfig(level=logging.DEBUG)
	myapp = MainWin()
	myapp.show()
	app.exec_()
