#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import QTime, QTimer

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
		self.ui.btnCancel.clicked.connect(self.ui_handleClick_btnCancel)

	def load(self):
		logging.debug('Loading GameModule')

		self.gameStartTime = QTime.currentTime()
		self.timerUpdateChrono.start(1000)

		self.score1 = 0
		self.score2 = 0

	def unload(self):
		logging.debug('Unloading GameModule')
		del self.gameStartTime
		self.timerUpdateChrono.stop()
	
	def other(self, **kwargs):
		logging.debug('Other GameModule')

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
