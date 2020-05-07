#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging, math

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
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

		db = Database.instance()
		if self.scores[Side.Left]>self.scores[Side.Right]:
			self.winSide=Side.Left
		elif self.scores[Side.Left]<self.scores[Side.Right]:
			self.winSide=Side.Right
		else:
			self.winSide = Side.Undef

		self.displayPlayers()
		if not any(team.hasGuest() for team in self.teams.values()):
			db.insertMatch(int(self.start_time), int(self.duration), self.teams[Side.Left].id, self.scores[Side.Left], self.teams[Side.Right].id, self.scores[Side.Right])
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
		losSide = self.winSide.opposite()
		picSize = {self.winSide:225, losSide:150,  'N':200}
		teamFont = {self.winSide:36, losSide:28,  'N':32}
		scoreFont = {self.winSide:100, losSide:80,  'N':90}
		self.ui.lblTeamNameL.setText(self.teams[Side.Left].name)
		self.ui.lblTeamNameR.setText(self.teams[Side.Right].name)
		self.ui.lblScoreL.setText(str(self.scores[Side.Left]))
		self.ui.lblScoreR.setText(str(self.scores[Side.Right]))
		
		baseFont = self.ui.lblTeamNameL.font()
		
		self.teams[Side.Left].players[0].displayImg(self.ui.imgP1L)
		if self.teams[Side.Left].size()==2:
			self.teams[Side.Left].players[0].displayImg(self.ui.imgP2L)
			self.ui.imgP2L.setVisible(True)
		else:
			self.ui.imgP2L.setVisible(False)
		
		self.teams[Side.Right].players[0].displayImg(self.ui.imgP1R)
		if self.teams[Side.Right].size()==2:
			self.teams[Side.Right].players[0].displayImg(self.ui.imgP2R)
			self.ui.imgP2R.setVisible(True)
		else:
			self.ui.imgP2R.setVisible(False)
			

		if self.winSide == Side.Undef:
			#Tie Game - All item of same size
			self.ui.lblTitle.setText("Tie Game!")
			#Updating FontSize of Team and Score labels
			baseFont.setPointSize(teamFont['N'])
			self.ui.lblTeamNameL.setFont(baseFont)
			self.ui.lblTeamNameR.setFont(baseFont)
			baseFont.setPointSize(scoreFont['N'])
			self.ui.lblScoreL.setFont(baseFont)
			self.ui.lblScoreR.setFont(baseFont)
			#Updating picture's size
			self.ui.imgP1L.setFixedSize(picSize['N'], picSize['N'])
			self.ui.imgP2L.setFixedSize(picSize['N'], picSize['N'])
			self.ui.imgP1R.setFixedSize(picSize['N'], picSize['N'])
			self.ui.imgP2R.setFixedSize(picSize['N'], picSize['N'])
			
		else:
			self.ui.lblTitle.setText("Congratulations!")		
			#Updating FontSize of Team and Score labels
			baseFont.setPointSize(teamFont[Side.Left])
			self.ui.lblTeamNameL.setFont(baseFont)
			baseFont.setPointSize(teamFont[Side.Right])
			self.ui.lblTeamNameR.setFont(baseFont)
			baseFont.setPointSize(scoreFont[Side.Left])
			self.ui.lblScoreL.setFont(baseFont)
			baseFont.setPointSize(scoreFont[Side.Right])
			self.ui.lblScoreR.setFont(baseFont)

			#Updating picture's size
			self.ui.imgP1L.setFixedSize(picSize[Side.Left], picSize[Side.Left])
			self.ui.imgP2L.setFixedSize(picSize[Side.Left], picSize[Side.Left])
			self.ui.imgP1R.setFixedSize(picSize[Side.Right], picSize[Side.Right])
			self.ui.imgP2R.setFixedSize(picSize[Side.Right], picSize[Side.Right])

			


	def eloProbability(self, rating1, rating2):
		return 1.0 / (1 + math.pow(10, (rating2 - rating1) / 400))

	def newEloRating(self):
		if self.winSide != Side.Undef: #No ex-aequo
			winners = self.teams[self.winSide].players
			losers = self.teams[self.winSide.opposite()].players
			ratingWinner = int(sum(p.eloRating for p in winners)/self.teams[self.winSide].size())
			ratingLoser = int(sum(p.eloRating for p in losers)/self.teams[self.winSide.opposite()].size())
			
			for player in winners:
				player.eloRating += int(80*(1-self.eloProbability(ratingWinner, ratingLoser)))
			for player in losers:
				player.eloRating -= int(80*(self.eloProbability(ratingLoser, ratingWinner)))

			for player in winners + losers:
				Database.instance().setEloRating(player.login, player.eloRating)

	def handleQuit(self):
		self.switchModule(modules.MenuModule)
