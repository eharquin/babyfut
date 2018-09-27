#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sys
import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime

from main_ui import Ui_MainWindow
from panels import MenuPanel, GamePanel, OptionsPanel

class MainWin(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.ui.panels.addWidget(MenuPanel(self))
		self.ui.panels.addWidget(GamePanel(self))
		self.ui.panels.addWidget(OptionsPanel(self))
		self.ui.panels.setCurrentIndex(0)

		self.displaySystemTime()
		self.startTimer(1000)

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