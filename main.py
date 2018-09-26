#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: limalayla
"""
import sys

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from math import ceil

from PyQt5.QtCore import QTime
from PyQt5 import QtWidgets
from main_ui import Ui_MainWindow

class MainWin(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()

		# UI Setup
		self.ui.setupUi(self)
		self.displaySystemTime()
		self.startTimer(1000)

		# Button connections
		self.ui.btnStart.clicked.connect(self.ui_handleClick_btnStart)
		self.ui.btnOptions.clicked.connect(self.ui_handleClick_btnOptions)
		self.ui.btnExit.clicked.connect(self.ui_handleClick_btnExit)

	def timerEvent(self, e): 
		self.displaySystemTime()

	def displaySystemTime(self):
		self.ui.lcdNumber.display(QTime.currentTime().toString("hh:mm:ss"))

	def ui_handleClick_btnStart(self):
		print('start')

	def ui_handleClick_btnOptions(self):
		print('options')

	def ui_handleClick_btnExit(self):
		print('exit')
		self.close()

if __name__=='__main__':
	app = QtWidgets.QApplication(sys.argv)
	myapp = MainWin()
	myapp.show()
	app.exec_()
