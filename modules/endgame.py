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

from player import Side
from module import Module
import modules
from ui.endgame_ui import Ui_Form as GameWidget

class EndGameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, GameWidget())
		self.screenTimeout = QTimer()
		self.screenTimeout.timeout.connect(self.handleQuit)
		self.screenTimeout.setSingleShot(True)

	def load(self):
		logging.debug('Loading EndGameModule')
		
		if len(self.players[self.winSide])>1:
			self.ui.lblP2_2.setText('{} Side'.format(self.winSide.name))
		
		for side in [Side.Left, Side.Right]:
			for player in self.players[side]:
				player.victories    += 1 if side==self.winSide else 0
				player.goals_scored += self.scores[side]
				player.time_played  += self.time
				player.games_played += 1
				player.save()
		
		# Quit the screen after 5 seconds if the user doesn't do it before
		#self.screenTimeout.start(5000)

	def unload(self):
		logging.debug('Unloading EndGameModule')
		self.screenTimeout.stop()
		del self.players
		del self.winSide
	
	def other(self, **kwargs):
		logging.debug('Other EndGameModule')
		
		for key, val in kwargs.items():
			if key=='players':
				self.players = val
			elif key=='winSide':
				self.winSide = val
			elif key=='scores':
				self.scores = val
			elif key=='time':
				self.time = val
		#else:
		#	raise ValueError('Unknown message identifier {}'.format(kwargs)
		
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Return:
			self.handleQuit()
	
	def handleQuit(self):
		self.switchModule(modules.MenuModule)
