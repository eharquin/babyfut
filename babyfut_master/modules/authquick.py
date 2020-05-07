#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifications : Yoann Malot, Thibaud Le Graverend
"""

import logging, csv, random
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import QSizePolicy, QDialog

from .auth import AuthModuleBase
from ..core.player import Player
from ..core.team import Team, TeamName, KeyboardWidget, ConstructTeam
from common.side import Side
from ..ui.authquick_ui import Ui_Form as AuthQuickWidget

from ..core.database import Database
from ..babyfut_master import getContent


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *



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
		self.updateSides(Side.Left)
		self.updateSides(Side.Right)
		
		self.ui.lblStarting.setVisible(False)
		
	def unload(self):
		logging.debug('Unloading AuthQuickModule')
		self.startingGameTimer.stop()
		super().unload()

	def createTeamList(self):
		self.teams = {Side.Left: ConstructTeam(self), Side.Right: ConstructTeam(self)}

	def _timerHandler(self):
		self.timerCount = self.timerCount -1
		self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
		if self.timerCount<=0:
			self.startingGameTimer.stop()
			self.handleDone()
		
	def addPlayer(self, side, player):
		if self.teams[side].size()<2:
			self.teams[side] = self.teams[side].addPlayer(player)
			self.updateSides(side)
			if all(isinstance(t, Team) for t in self.teams.values()):
				self.timerCount = 5
				self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
				self.ui.lblStarting.setVisible(True)
				self.startingGameTimer.start(1000)

		

	def changeTeamName(self, side):
		lblTeamName = {Side.Left:self.ui.lblTeamLeft, Side.Right:self.ui.lblTeamRight}
		lblTeamName[side].setText(self.teams[side].name)

	def updateSides(self, side):
		
		widgetPlayerTop = {Side.Left:self.ui.imgP1, Side.Right:self.ui.imgP3 }
		labelPlayerTop = {Side.Left:self.ui.lblP1, Side.Right:self.ui.lblP3 }
		widgetPlayerBottom = {Side.Left:self.ui.imgP2, Side.Right:self.ui.imgP4 }
		labelPlayerBottom = {Side.Left:self.ui.lblP2, Side.Right:self.ui.lblP4 }
		lblTeamName = {Side.Left:self.ui.lblTeamLeft, Side.Right:self.ui.lblTeamRight}

		if self.teams[side].size()==1:
			self.teams[side].players[0].displayImg(widgetPlayerTop[side])
			widgetPlayerTop[side].setFixedSize(self.bigPicSize, self.bigPicSize)
			labelPlayerTop[side].setText(self.teams[side].players[0].name)
			widgetPlayerBottom[side].setVisible(False)
			labelPlayerBottom[side].setVisible(False)
			lblTeamName[side].setVisible(False)
			
		elif self.teams[side].size()==2:
			widgetPlayerTop[side].setFixedSize(self.smallPicSize, self.smallPicSize)
			self.teams[side].players[1].displayImg(widgetPlayerBottom[side])
			labelPlayerBottom[side].setText(self.teams[side].players[1].name)
			widgetPlayerBottom[side].setVisible(True)
			labelPlayerBottom[side].setVisible(True)
			lblTeamName[side].setVisible(True)
			self.changeTeamName(side)
