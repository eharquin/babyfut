#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt

from .. import modules
from ..core.database import Database
from ..core.player import Player
from common.side import Side
from ..core.module import Module
from ..ui.endgame_ui import Ui_Form as EndGameWidget

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
			if Player.playerGuest() in self.players[side]:
				idTeams[side] = db.select_guest_team()
			else:
				idTeams[side] = db.insert_team([player.id for player in self.players[side]], self.scores[side])

		db.insertMatch(int(self.start_time), int(self.duration), idTeams[self.winSide], idTeams[self.winSide.opposite()])

		# Quit the screen after 5 seconds if the user doesn't do it before
		#self.screenTimeout.start(5000)

	def unload(self):
		logging.debug('Unloading EndGameModule')
		self.screenTimeout.stop()

		del self.players
		del self.gameType
		del self.winSide
		del self.scores
		del self.start_time
		del self.duration

	def other(self, **kwargs):
		logging.debug('Other EndGameModule')

		for key, val in kwargs.items():
			if key=='players':
				self.players = val
			elif key=='gameType':
				self.gameType = val
			elif key=='winSide':
				self.winSide = val
			elif key=='scores':
				self.scores = val
			elif key=='start_time':
				self.start_time = val
			elif key=='duration':
				self.duration = val

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Return:
			self.handleQuit()

	def setActiveP2(self, active):
		#Organise Widgets for display either 1 or 2 Players

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
			players[1].displayImg(self.ui.ImgP2)
			self.ui.lblP2.setText(players[1].name)


	def handleQuit(self):
		self.switchModule(modules.MenuModule)
