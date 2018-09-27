#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtGui import QRegion
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox

from menu_ui import Ui_Form as Menu_Form
from game_ui import Ui_Form as Game_Form
from options_ui import Ui_Form as Options_Form

class Panel(QtWidgets.QWidget):
	def __init__(self, parent=None, form=None):
		Panel.__dict_panels = {MenuPanel: 0, GamePanel: 1, OptionsPanel: 2}

		# UI Setup
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = form
		self.ui.setupUi(self)
		self.parentWin = parent

	def switchPanel(self, newType):
		panelIndex = Panel.__dict_panels.get(newType)
		if panelIndex!=None:
			self.parentWin.ui.panels.currentWidget().unload()
			self.parentWin.ui.panels.setCurrentIndex(panelIndex)
			self.parentWin.ui.panels.currentWidget().load()
		else:
			logging.error('Error: unknown panel {} in {}'.format(newType, self.__dict_panels))

	def load(self):
		logging.warning('Unimplemented method')

	def unload(self):
		logging.warning('Unimplemented method')

class MenuPanel(Panel):
	def __init__(self, parent=None):
		super().__init__(parent, Menu_Form())

		# Button connections
		self.ui.btn0Start.clicked.connect(self.ui_handleClick_btnStart)
		self.ui.btn1Options.clicked.connect(self.ui_handleClick_btnOptions)
		self.ui.btn2Exit.clicked.connect(self.ui_handleClick_btnExit)

	def load(self):
		logging.debug('Loading MenuPanel')

	def unload(self):
		logging.debug('Unloading MenuPanel')

	def ui_handleClick_btnStart(self):
		logging.debug('start')
		self.switchPanel(GamePanel)

	def ui_handleClick_btnOptions(self):
		self.switchPanel(OptionsPanel)

	def ui_handleClick_btnExit(self):
		logging.debug('exit')
		self.parentWin.close()

class GamePanel(Panel):
	def __init__(self, parent=None):
		super().__init__(parent, Game_Form())

		# Button setup
		#print(str(self.ui.btnScore1.rect()))
		#print(str(self.ui.btnScore2.rect()))
		#region = QRegion(self.ui.btnScore1.rect(), QRegion.Ellipse);
		#self.ui.btnScore1.setMask(region);
		#self.ui.btnScore2.setMask(region);

		# Timer managment
		self.timerUpdateChrono = QTimer(self)
		self.timerUpdateChrono.timeout.connect(self.updateChrono)

		# Button connections
		self.ui.btnScore1.clicked.connect(self.ui_handleClick_btnScore1)
		self.ui.btnScore2.clicked.connect(self.ui_handleClick_btnScore2)
		self.ui.btnCancel.clicked.connect(self.ui_handleClick_btnCancel)

	def load(self):
		logging.debug('Loading GamePanel')

		self.gameStartTime = QTime.currentTime()
		self.timerUpdateChrono.start(1000)

		self.score1 = 0
		self.score2 = 0

	def unload(self):
		logging.debug('Unloading GamePanel')
		del self.gameStartTime
		self.timerUpdateChrono.stop()

	def updateChrono(self):
		# Updated each second
		elapsedSec = self.gameStartTime.secsTo(QTime.currentTime())
		self.ui.lcdChrono.display(QTime(0,0).addSecs(elapsedSec).toString("hh:mm:ss"))

	def updateScores(self):
		self.ui.btnScore1.setText(str(self.score1))
		self.ui.btnScore2.setText(str(self.score2))

	def ui_handleClick_btnScore1(self):
		self.score1 += 1
		self.updateScores()

	def ui_handleClick_btnScore2(self):
		self.score2 += 1
		self.updateScores()

	def ui_handleClick_btnCancel(self):
		self.switchPanel(MenuPanel)

class OptionsPanel(Panel):
	def __init__(self, parent=None):
		super().__init__(parent, Options_Form())

		# Button connections
		self.ui.btnSave.clicked.connect(self.ui_handleClick_btnSave)
		self.ui.btnBack.clicked.connect(self.ui_handleClick_btnBack)

	def load(self):
		logging.debug('Loading OptionsPanel')
		cbb = QComboBox()
		cbb.addItem('true')
		cbb.addItem('false')
		self.ui.options.insertRow(self.ui.options.rowCount())
		self.ui.options.setItem(self.ui.options.rowCount()-1, 0, QTableWidgetItem('FullScreen'))
		print(self.ui.options.rowCount()-1, 1, cbb)
		self.ui.options.setCellWidget(self.ui.options.rowCount()-1, 1, cbb)

	def unload(self):
		logging.debug('Unloading OptionsPanel')
		# Delete the table's content
		self.ui.options.setRowCount(0)

	def ui_handleClick_btnSave(self):
		print(self.ui.options.rowCount(), self.ui.options.columnCount())
		print(self.ui.options.cellWidget(0, 0))
		print(self.ui.options.cellWidget(0, 1))
		print(self.ui.options.cellWidget(1, 0))
		print(self.ui.options.cellWidget(1, 1))
		print(self.ui.options.cellWidget(2, 1))
		print(self.ui.options.cellWidget(1, 2))
		if self.ui.options.cellWidget(0, 1).currentText().lower() == 'true':
			self.parentWin.showFullScreen()
		else:
			self.parentWin.showNormal()

		self.switchPanel(MenuPanel)

	def ui_handleClick_btnBack(self):
		# ToDo: Maybe add a warning
		self.switchPanel(MenuPanel)