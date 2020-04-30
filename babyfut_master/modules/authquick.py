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
from common.side import Side
from ..ui.authquick_ui import Ui_Form as AuthQuickWidget
from ..ui.team_name_dialog_ui import Ui_Dialog as TeamNameDialog
from ..core.database import Database
from ..babyfut_master import getContent


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

		if len(self.players[side])==2:
			db = Database.instance()
			if (not db.checkTeam(self.players[side])):
				print('coucou')
				self.getTeamName = TeamName(self, self.players[side])
				self.getTeamName.open()


		# Display 
		# if len(self.players[Side.Left])==2 and len(self.players[Side.Right])==2:			
		# 	self.timerCount = 5
		# 	self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
		# 	self.ui.lblStarting.setVisible(True)
		# 	self.startingGameTimer.start(1000)

	#def getTeamName(self):




	def updateSides(self, side):
		
		widgetPlayerTop = {Side.Left:self.ui.imgP1, Side.Right:self.ui.imgP3 }
		labelPlayerTop = {Side.Left:self.ui.lblP1, Side.Right:self.ui.lblP3 }
		widgetPlayerBottom = {Side.Left:self.ui.imgP2, Side.Right:self.ui.imgP4 }
		labelPlayerBottom = {Side.Left:self.ui.lblP2, Side.Right:self.ui.lblP4 }
		lblTeamName = {Side.Left:self.ui.lblTeamLeft, Side.Right:self.ui.lblTeamRight}

		if len(self.players[side])==1:
			self.players[side][0].displayImg(widgetPlayerTop[side])
			widgetPlayerTop[side].setFixedSize(self.bigPicSize, self.bigPicSize)
			labelPlayerTop[side].setText(self.players[side][0].name)
			widgetPlayerBottom[side].setVisible(False)
			labelPlayerBottom[side].setVisible(False)
			lblTeamName[side].setVisible(False)
			
		elif len(self.players[side])==2:
			widgetPlayerTop[side].setFixedSize(self.smallPicSize, self.smallPicSize)
			self.players[side][1].displayImg(widgetPlayerBottom[side])
			labelPlayerBottom[side].setText(self.players[side][1].name)
			# lblTeamName[side].setText
			widgetPlayerBottom[side].setVisible(True)
			labelPlayerBottom[side].setVisible(True)
			lblTeamName[side].setVisible(True)


class TeamName(QDialog):
	def __init__(self, parent, players):
		QDialog.__init__(self, parent)
		self.ui = TeamNameDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Create a team')
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(players[0].fname, players[1].fname))
		self.ui.nameInupt.setText(self.setRandomName())
		# self.ex = KeyboardUI()
		# self.ex.show()

	def setRandomName(self):
		wordsPath = getContent('words.csv')
		adjectivesPath = getContent('adjectives.csv')

		wordsFile = open(wordsPath, newline='')
		wordsContent = csv.reader(wordsFile, delimiter=';')
		wordsList = [row for row in wordsContent]
		word = wordsList[random.randint(0, len(wordsList))]

		adjectivesFile = open(adjectivesPath, newline='')
		adjectivesContent = csv.reader(adjectivesFile, delimiter=';')
		adjectivesList = [row for row in adjectivesContent]
		if word[1]=='masc':
			adjective = adjectivesList[random.randrange(0, len(adjectivesList))][0]
		elif word[1]=='fem':
			adjective = adjectivesList[random.randrange(0, len(adjectivesList))][1]
		
		wordsFile.close()
		adjectivesFile.close()
		return str('Les ' + word[0] + ' ' + adjective)


### Keyboard from https://gist.github.com/arunreddy/ee01b4ccdd1f2e5773cdd5352783d9c6
