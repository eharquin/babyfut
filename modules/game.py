#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegion
from PyQt5.QtCore import QTime, QTimer, QRect, Qt

from module import Module
import modules
from ui.game_ui import Ui_Form as GameWidget

class GameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, GameWidget())

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

	def load(self):
		logging.debug('Loading GameModule')

		self.gameStartTime = QTime.currentTime()
		self.timerUpdateChrono.start(1000)
		self.ui.lcdChrono.display(QTime(0,0).toString("hh:mm:ss"))

		self.score1 = 0
		self.score2 = 0
		self.updateScores()

	def unload(self):
		logging.debug('Unloading GameModule')
		del self.gameStartTime
		self.timerUpdateChrono.stop()
	
	def other(self, **kwargs):
		logging.debug('Other GameModule')
	
	def resizeEvent(self, event):
		# 40% of the window width to have (5% margin)-(40% circle)-(10% middle)-(40% circle)-(5% margin)
		btnDiameter = self.parent_win.width()*0.4
		region = QRegion(QRect(0, 0, btnDiameter, btnDiameter), QRegion.Ellipse)
		self.ui.btnScore1.setMinimumSize(btnDiameter, btnDiameter)
		self.ui.btnScore2.setMinimumSize(btnDiameter, btnDiameter)
		self.ui.btnScore1.setMask(region)
		self.ui.btnScore2.setMask(region)
		
		QtWidgets.QWidget.resizeEvent(self, event)

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.ui_handleClick_btnCancel()
		elif e.key() == Qt.Key_Left:
			self.ui_handleClick_btnScore1()
		elif e.key() == Qt.Key_Right:
			self.ui_handleClick_btnScore2()

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
		self.switchModule(modules.MenuModule)
