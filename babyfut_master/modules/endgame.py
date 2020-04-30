#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging, math

from PyQt5 import QtWidgets

from .. import modules
from ..core.database import Database
from ..core.player import Player
from common.side import Side
from ..core.module import Module
from ..ui.endgame_ui import Ui_Form as EndGameWidget

class EndGameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, EndGameWidget())

	def load(self):
		logging.debug('Loading EndGameModule')

		self.displayPlayers()

		db = Database.instance()
		
		if not any(team.hasGuest() for team in self.teams.values()):
			db.insertMatch(int(self.start_time), int(self.duration), self.teams[self.winSide].id, self.scores[self.winSide], self.teams[self.winSide.opposite()].id, self.scores[self.winSide.opposite()])
			self.newEloRating()
	
	def unload(self):
		logging.debug('Unloading EndGameModule')

		del self.teams
		del self.gameType
		del self.winSide
		del self.scores
		del self.start_time
		del self.duration

	def other(self, **kwargs):
		logging.debug('Other EndGameModule')

		for key, val in kwargs.items():
			if key=='teams':
				self.teams = val
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

	def displayPlayers(self):
		players = self.teams[self.winSide].players

		players[0].displayImg(self.ui.imgP1)
		self.ui.lblP1.setText(players[0].name)

		spacer = self.ui.horizontalLayout.itemAt(2).spacerItem()
		if self.teams[self.winSide].size()==2:
			players[1].displayImg(self.ui.imgP2)
			self.ui.lblP2.setText(players[1].name)
			self.ui.widgetLayoutP2.setVisible(True)
			spacer.changeSize(80, spacer.geometry().height(), QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		else:
			self.ui.widgetLayoutP2.setVisible(False)
			spacer.changeSize(0, spacer.geometry().height(), QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)


	def eloProbability(self, rating1, rating2):
		return 1.0 / (1 + math.pow(10, (rating2 - rating1) / 400))

	def newEloRating(self):
		winners = self.teams[winSide].players
		losers = self.teams[winSide.opposite()].players
		ratingWinner = int(sum(p.eloRating for p in winners/self.teams[winSide].size()))
		ratingLoser = int(sum(p.eloRating for p in losers/self.teams[winSide.opposite()].size()))
		
		for player in winners:
			player.eloRating += 80*(1-self.eloProbability(ratingWinner, ratingLoser))
		for player in losers:
			player.eloRating -= 80*(self.eloProbability(ratingLoser, ratingWinner))

		for player in winners + losers:
			Database.instance().setEloRating(player.login, player.eloRating)

	def handleQuit(self):
		self.switchModule(modules.MenuModule)
