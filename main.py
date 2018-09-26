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
from menu_ui import Ui_Form as Menu_Form
from options_ui import Ui_Form as Options_Form

class MainWin(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.switchPanel(MenuPanel(self))

	def timerEvent(self, e): 
		self.displaySystemTime()

	def displaySystemTime(self):
		self.ui.lcdNumber.display(QTime.currentTime().toString("hh:mm:ss"))

	def switchPanel(self, panel):
		print("switching from {} to {} (size {})".format(self.ui.stackedWidget.currentWidget(), panel, self.ui.stackedWidget.count()))
		#self.ui.panel = panel
		self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
		self.ui.stackedWidget.addWidget(panel)
		self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.count()-1)

class MenuPanel(QtWidgets.QWidget):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)

		# UI Setup
		self.ui = Menu_Form()
		self.ui.setupUi(self)
		#self.displaySystemTime()
		#self.startTimer(1000)

		# Button connections
		self.ui.btn0Start.clicked.connect(self.ui_handleClick_btnStart)
		self.ui.btn1Options.clicked.connect(self.ui_handleClick_btnOptions)
		self.ui.btn2Exit.clicked.connect(self.ui_handleClick_btnExit)

	def ui_handleClick_btnStart(self):
		print('start')
		self.parent().parent().parent().showFullScreen()

	def ui_handleClick_btnOptions(self):
		print('options', self.parent(), self.parent().parent(), self.parent().parent().parent())
		self.parent().parent().parent().switchPanel(OptionsPanel(self.parent().parent().parent()))

	def ui_handleClick_btnExit(self):
		print('exit')
		self.parent().parent().parent().close()

class OptionsPanel(QtWidgets.QWidget):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)

		# UI Setup
		self.ui = Options_Form()
		self.ui.setupUi(self)

		# Button connections
		self.ui.btnBack.clicked.connect(self.ui_handleClick_btnBack)

	def ui_handleClick_btnBack(self):
		print('back', self.parent(), self.parent().parent(), self.parent().parent().parent())
		self.parent().parent().parent().switchPanel(MenuPanel(self.parent().parent().parent()))

if __name__=='__main__':
	app = QtWidgets.QApplication(sys.argv)
	myapp = MainWin()
	myapp.show()
	app.exec_()
