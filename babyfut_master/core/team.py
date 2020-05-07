#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging
import sys
import csv, random
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent, QSignalMapper
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

from ..babyfut_master import getMainWin, getContent
from .player import Player
from .database import Database, DatabaseError
from ..ui.team_name_dialog_ui import Ui_Dialog as TeamNameDialog


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

	def getNameDialog(self, parentWidget, random=False):
		if self.size()==2:
			dialog = TeamName(parentWidget, self, random)
			dialog.exec()

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
	def __init__(self, parent, team, welcome=False):
		QDialog.__init__(self, parent)
		self.parent = parent
		self.team = team
		self.ui = TeamNameDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Set your team name')
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(team.players[0].fname, team.players[1].fname))
		name = self.setRandomName() if welcome else team.name
		self.ui.nameInput.setText(name)
		self.ui.nameInput.setReadOnly(True)
		self.keyboard = KeyboardWidget(self, name, welcome)
		if welcome:
			self.keyboard.hide()
		else:
			self.keyboard.show()

		self.ui.editName.clicked.connect(self.keyboard.show)
		self.ui.enter.clicked.connect(self.finish)
		self.ui.enter.setDefault(True)

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

	def insertTeam(self):
		db = Databse.instance()
		db.insertTeam


class KeyboardWidget(QWidget):
	def __init__(self, parent, name, welcome=False):
		super(KeyboardWidget, self).__init__(parent)
		self.parent = parent
		self.oldName=name
		self.welcome = welcome #If not welcome, Keyboard is autonomous and must close when done
		self.signalMapper = QSignalMapper(self)
		self.signalMapper.mapped[int].connect(self.buttonClicked)
		self.setGeometry(0, 0, parent.width(), parent.height())
		self.initUI()

	def initUI(self):
		self.verticalLayout = QVBoxLayout()
		self.layout = QGridLayout()

		self.title = QLabel("How should we call you ?")
		self.title.setFont(QFont('Arial', 25))
		self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter)

		self.setAutoFillBackground(True)
		self.text_box = QLineEdit()
		self.text_box.setReadOnly(True)
		self.text_box.setMaxLength(30)
		self.text_box.setFont(QFont('Arial', 20))
		if not self.welcome:
			self.text_box.setText(self.oldName)

		self.verticalLayout.addWidget(self.text_box)

		self.maj = True
		self.namesMaj = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
						'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
						'Q', 'S', 'D','F', 'G', 'H', 'J', 'K', 'L', 'M', 
						'W', 'X', 'C', 'V', 'B', 'N', '?', '!', '.', '-']
		
		self.namesMin =  ['é', 'è', 'à', 'ç', '(', ')', '[', ']', '_', '@',
						'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
						'q', 's', 'd','f', 'g', 'h', 'j', 'k', 'l', 'm',
						'w', 'x', 'c', 'v', 'b', 'n',"'",';',':','/']

		self.positions = [(i, j) for i in range(4) for j in range(10)]

		for position, name in zip(self.positions, self.namesMaj):

			if name == '':
				continue
			button = QPushButton(name)
			button.setFont(QFont('Arial', 20))
			button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			button.KEY_CHAR = ord(name)
			button.clicked.connect(self.signalMapper.map)
			self.signalMapper.setMapping(button, button.KEY_CHAR)
			self.layout.addWidget(button, *position)


		# Cancel button
		cancel_button = QPushButton('Cancel')
		cancel_button.setFont(QFont('Arial', 20))
		cancel_button.KEY_CHAR = Qt.Key_Cancel
		self.layout.addWidget(cancel_button, 5, 0, 1, 2)
		cancel_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(cancel_button, cancel_button.KEY_CHAR)
		cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Maj button
		maj_button = QPushButton('MAJ')
		maj_button.setFont(QFont('Arial', 20))
		maj_button.KEY_CHAR = Qt.Key_Shift
		self.layout.addWidget(maj_button, 5, 2, 1, 2)
		maj_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(maj_button, maj_button.KEY_CHAR)
		maj_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Space button
		space_button = QPushButton('Space')
		space_button.setFont(QFont('Arial', 20))
		space_button.KEY_CHAR = Qt.Key_Space
		self.layout.addWidget(space_button, 5, 4, 1, 2)
		space_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
		space_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		# Back button
		back_button = QPushButton('Back')
		back_button.setFont(QFont('Arial', 20))
		back_button.KEY_CHAR = Qt.Key_Backspace
		self.layout.addWidget(back_button, 5, 6, 1, 2)
		back_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
		back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


		# Done button
		done_button = QPushButton('Done')
		done_button.setFont(QFont('Arial', 20))
		done_button.KEY_CHAR = Qt.Key_Home
		self.layout.addWidget(done_button, 5, 8, 1, 2)
		done_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
		done_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Insert Grid in Vertical Layout
		self.verticalLayout.insertLayout(3,self.layout)
		self.setLayout(self.verticalLayout)


	def convertLetters(self):
		# Check what is the actual keyboard
		if self.maj==True:
			names=self.namesMin
			self.maj=False
		else:
			names = self.namesMaj
			self.maj=True
		# Changes button placeholder and add new mapping
		for i in range(0, len(names)):
			row, col, rowspan, colspan = self.layout.getItemPosition(i)
			self.layout.itemAtPosition(row, col).widget().setText(names[i])
			self.layout.itemAtPosition(row, col).widget().KEY_CHAR = ord(names[i])
			self.signalMapper.setMapping(self.layout.itemAtPosition(row, col).widget(), self.layout.itemAtPosition(row, col).widget().KEY_CHAR)

			

	def buttonClicked(self, char_ord):

		txt = self.text_box.text()

		if char_ord == Qt.Key_Backspace:
			txt = txt[:-1]
			if len(txt)==0 and not self.maj:
				self.convertLetters()
		elif char_ord == Qt.Key_Home:
			self.parent.ui.nameInput.setText(txt)
			self.parent.ui.nameInput.setFocusPolicy(Qt.NoFocus)
			self.parent.setFocus()
			self.parent.ui.enter.setDefault(True)
			if self.welcome:
				self.hide()
			else:
				self.parent.finish()
			return
		elif char_ord == Qt.Key_Shift:
			self.convertLetters()
		elif char_ord == Qt.Key_Space:
			txt += ' '
		elif char_ord == Qt.Key_Cancel:
			self.parent.setFocus()
			self.parent.ui.enter.setDefault(True)
			if self.welcome:
				self.hide()
			else:
				self.parent.finish()
			return
		else:
			txt += chr(char_ord)
			if len(txt) == 1 and self.maj:
				self.convertLetters()

		self.setFocus()
		self.text_box.setText(txt)

		# if len(self.text_box.text())==1:
		# 	self.convertLetters()
