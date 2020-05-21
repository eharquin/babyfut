#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann MALOT, Thibaud LE GRAVEREND
"""

import os
import logging
import sys
import csv, random
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent, QSignalMapper
from PyQt5.QtWidgets import *


from ..babyfut_master import getMainWin, getContent
from .player import Player
from .database import Database, DatabaseError
from ..ui.team_name_dialog_ui import Ui_Dialog as TeamNameDialog
from ..ui.keyboard import KeyboardWidget, KeyboardDialog

class AbstractTeam(QObject):
	def __init__(self):
		QObject.__init__(self)
		self.players = list()
 
	def size(self):
		return len(self.players)

	def hasPlayer(self, player):
		return any(p.login == player.login for p in self.players)
	
	def hasGuest(self):
		return self.hasPlayer(Player.playerGuest())

class ConstructTeam(AbstractTeam):

	def __init__(self, parentWidget):
		super().__init__()
		self.players.append(Player.playerGuest())
		self.parent = parentWidget

	def addPlayer(self, player):
		if player==Player.playerGuest():
			return

		if Player.playerGuest() in self.players:
			self.players.remove(Player.playerGuest())
		
		if len(self.players)<2:
			self.players.append(player)
		
		if len(self.players)==2:
			return self.validateTeam()
		else:
			return self

	def validateTeam(self):
		if Player.playerGuest() in self.players:
			return Team.teamGuest()
		else:
			logins = [p.login for p in self.players]
			result = Database.instance().checkTeam(*logins)
			if result:
				return Team(result[0], result[1], self.players)
			else:
				name = "Unnamed Team" if self.size()==2 else None
				id = self._insertDB(name)
				validatedTeam = Team(id, name, self.players)
				validatedTeam.getNameDialog(self.parent, True)
				return validatedTeam


	def _insertDB(self, name):
		db = Database.instance()
		if len(self.players)==2:
			id= db.insertTeam(self.players[0].login, self.players[1].login, name)
		elif len(self.players)==1:
			self._name=None
			id= db.insertTeam(self.players[0].login)
		return id


class Team(AbstractTeam):
	_teamGuest = None
	def __init__(self, id, name, players):
		super().__init__()
		if len(players)==2 or (len(players)==1 and name==None):
			self.players=players
			self._name = name
			self.id = id

	def setName(self, name):
		if self.size()==2:
			self._name = name
			Database.instance().setTeamName(self.id, self._name)

	def getNameDialog(self, parentWidget, welcome=False):
		if self.size()==2:
			if welcome:
				dialog = TeamName(parentWidget, self)
				dialog.exec()
			else:
				dialog=KeyboardDialog(parentWidget, "Enter your new name", self.name)
				dialog.exec()
				result = dialog.getResult()
				if result:
					self.setName(result)

	@staticmethod
	def loadFromDB(id):
		players = list()
		team = Database.instance().selectTeam(id)
		players.append(Player.loadFromDB(team[2]))
		if team[3]:
			players.append(Player.loadFromDB(team[3]))
		return Team(team[0], team[1], players)

	@property
	def name(self):
		if self.size()==2:
			return self._name
		else:
			return self.players[0].name

	@staticmethod
	def teamGuest():
		if not Team._teamGuest:
			Team._teamGuest = Team(0, None, [Player.playerGuest()])
		return Team._teamGuest


class TeamName(QDialog):
	def __init__(self, parent, team):
		QDialog.__init__(self, parent)
		self.parent = parent
		self.team = team
		self.ui = TeamNameDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Set your team name')
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(team.players[0].fname, team.players[1].fname))
		name = self.setRandomName()
		self.ui.nameInput.setText(name)
		self.ui.nameInput.setReadOnly(True)
		self.keyboard = KeyboardWidget(self, "")
		self.keyboard.hide()

		self.ui.editName.clicked.connect(self.keyboard.show)
		self.ui.enter.clicked.connect(self.finish)
		self.ui.enter.setDefault(True)

	def keyboardResult(self, texte=None):
		if texte:
			self.ui.nameInput.setText(texte)

	def finish(self):
		self.team.setName(self.ui.nameInput.text())
		self.done(1)

	def setRandomName(self):
		wordsPath = getContent('words.csv')
		adjectivesPath = getContent('adjectives.csv')

		wordsFile = open(wordsPath, newline='')
		wordsContent = csv.reader(wordsFile, delimiter=';')
		wordsList = [row for row in wordsContent]
		word = wordsList[random.randrange(0, len(wordsList))]

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

	def resizeEvent(self, event):
		self.keyboard.resize(self.width(), self.height())	

	# def insertTeam(self):
	# 	db = Databse.instance()
	# 	db.insertTeam


