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

from database import Database, DatabaseError
from player import Side, PlayerGuest
from module import Module
import modules
from ui.endgame_ui import Ui_Form as EndGameWidget

class EndGameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, EndGameWidget())
		self.screenTimeout = QTimer()
		self.screenTimeout.timeout.connect(self.handleQuit)
		self.screenTimeout.setSingleShot(True)
		self.middleSpacerWidth = self.ui.horizontalLayout.itemAt(2).spacerItem().geometry().width()

	def load(self):
		logging.debug('Loading EndGameModule')
		
		self.setActiveP2(len(self.players[self.winSide])>1)
		self.displayPlayers()
		
		db = Database.instance()
		idTeams = {}
		
		for side in [Side.Left, Side.Right]:
			if PlayerGuest in self.players[side]:
				idTeams[side] = db.select_guest_team()
			else:
				idTeams[side] = db.insert_team([player.id for player in self.players[side]], self.scores[side])
		
		db.insert_match(int(self.start_time), int(self.duration), idTeams[self.winSide], idTeams[self.winSide.opposite]) 
		
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
			elif key=='start_time':
				self.start_time = val
				print('start_time {}'.format(val))
			elif key=='duration':
				self.duration = val
				print('duration {}'.format(val))
		#else:
		#	raise ValueError('Unknown message identifier {}'.format(kwargs)
	
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Return:
			self.handleQuit()
	
	def setActiveP2(self, active):
		self.ui.widgetLayoutP2.setVisible(active)
		spacer = self.ui.horizontalLayout.itemAt(2).spacerItem()
		
		if active:
			spacer.changeSize(self.middleSpacerWidth, spacer.geometry().height(), QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		else:
			spacer.changeSize(0, spacer.geometry().height(), QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
	
	def displayPlayers(self):
		players = self.players[self.winSide]
		
		players[0].displayImg(self.ui.imgP1)
		self.ui.lblP1.setText(players[0].name)
		
		if len(self.players[self.winSide])>1:
			players[1].displayImg(self.ui.imgP2)
			self.ui.lblP2.setText(players[1].name)
	
	def handleQuit(self):
		self.switchModule(modules.MenuModule)
