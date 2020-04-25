#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifications : Yoann Malot, Thibaud Le Graverend
"""

import logging
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import QSizePolicy

from .auth import AuthModuleBase
from ..core.player import Player
from common.side import Side
from ..ui.authquick_ui import Ui_Form as AuthQuickWidget

class AuthQuickModule(AuthModuleBase):
	def __init__(self, parent):
		super().__init__(parent, AuthQuickWidget())
		#Timer to start automatically the game when 4 players
		self.startingGameTimer = QTimer(self)
		self.startingGameTimer.timeout.connect(self._timerHandler)

		#Profile picture size
		self.smallPicSize = 200
		self.bigPicSize = 300

	def load(self):
		logging.debug('Loading AuthQuickModule')
		super().load()

		for side in [Side.Left, Side.Right]:
			if len(self.players[side])==0:
				self.addPlayer(side, Player.playerGuest())
		
		self.ui.lblStarting.setVisible(False)
		
	def unload(self):
		logging.debug('Unloading AuthQuickModule')
		super().unload()

	def createPlayerList(self):
		self.players = {Side.Left: list(), Side.Right: list()}

	def _timerHandler(self):
		self.timerCount = self.timerCount -1
		self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
		if self.timerCount<=0:
			self.startingGameTimer.stop()
			self.handleDone()
		
	def addPlayer(self, side, player):
		# If there is a placeholder Guest, clear it from the list, we don't need it anymore
		if len(self.players[side])>0 and self.players[side][0]==Player.playerGuest():
			self.players[side].clear()

		if len(self.players[side])<2:
			self.players[side].append(player)
			self.updateSides(side)

		# Display 
		if len(self.players[Side.Left])==2 and len(self.players[Side.Right])==2:			
			self.timerCount = 5
			self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
			self.ui.lblStarting.setVisible(True)
			self.startingGameTimer.start(1000)

	def updateSides(self, side):

		widgetLayoutTop = {Side.Left:self.ui.widgetLayoutP1, Side.Right:self.ui.widgetLayoutP3 }
		widgetLayoutBottom = {Side.Left:self.ui.widgetLayoutP2, Side.Right:self.ui.widgetLayoutP4 }
		widgetPlayerTop = {Side.Left:self.ui.imgP1, Side.Right:self.ui.imgP3 }
		labelPlayerTop = {Side.Left:self.ui.lblP1, Side.Right:self.ui.lblP3 }
		widgetPlayerBottom = {Side.Left:self.ui.imgP2, Side.Right:self.ui.imgP4 }
		labelPlayerBottom = {Side.Left:self.ui.lblP2, Side.Right:self.ui.lblP4 }

		if len(self.players[side])==1:
			self.players[side][0].displayImg(widgetPlayerTop[side])
			widgetPlayerTop[side].setFixedSize(self.bigPicSize, self.bigPicSize)
			labelPlayerTop[side].setText(self.players[side][0].name)
			widgetLayoutBottom[side].setVisible(False)
			
		elif len(self.players[side])==2:
			widgetPlayerTop[side].setFixedSize(self.smallPicSize, self.smallPicSize)
			self.players[side][1].displayImg(widgetPlayerBottom[side])
			labelPlayerBottom[side].setText(self.players[side][1].name)
			widgetLayoutBottom[side].setVisible(True)
			