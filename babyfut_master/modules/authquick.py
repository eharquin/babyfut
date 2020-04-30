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

import sys
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

			if len(self.players[side])==2:
				db = Database.instance()
				if (not db.checkTeam(self.players[side])):
					self.getTeamName = TeamName(self, self.players[side])
					self.getTeamName.open()

			self.updateSides(side)

		# Display 
		if len(self.players[Side.Left])==2 and len(self.players[Side.Right])==2:			
			self.timerCount = 5
			self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
			self.ui.lblStarting.setVisible(True)
			self.startingGameTimer.start(1000)


	def insertTeam(self, name, players):
		db = Database.instance()


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
			

class TeamName(QDialog):
	def __init__(self, parent, players):
		QDialog.__init__(self, parent)
		self.parent = parent
		self.players = players
		self.ui = TeamNameDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Create a team')
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(players[0].fname, players[1].fname))
		self.ui.nameInput.setText(self.setRandomName())
		self.ui.nameInput.setReadOnly(True)
		self.keyboard = KeyboardWidget(self)
		self.keyboard.hide()
		self.ui.editName.clicked.connect(self.keyboard.show)
		self.ui.enter.clicked.connect(self.sendName)

	def sendName(self):
		self.parent.insertTeam(self.ui.nameInput.text(), self.players)
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
	def __init__(self, parent=None):
		super(KeyboardWidget, self).__init__(parent)
		self.parent = parent
		self.signalMapper = QSignalMapper(self)
		self.signalMapper.mapped[int].connect(self.buttonClicked)
		self.setGeometry(0, 0, parent.width(), parent.height())
		self.initUI()

	def initUI(self):
		self.layout = QGridLayout()

		self.setAutoFillBackground(True)
		self.text_box = QLineEdit()
		self.text_box.setReadOnly(True)
		self.text_box.setFont(QFont('Arial', 20))

		self.layout.addWidget(self.text_box, 0, 0, 1, 13)

		self.maj = True
		self.namesMaj = ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D',
					'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W', 'X', 'C', 'V', 'B', 'N',
					'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '(', ')']
		
		self.namesMin =  ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd',
					'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n',
					'é', 'è', 'à', '!', '?', "'", 'ç', '@', '*', '<', '>', '_', '-']

		self.positions = [(i + 1, j) for i in range(3) for j in range(13)]

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
		self.layout.addWidget(space_button, 5, 5, 1, 3)
		space_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
		space_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		# Back button
		back_button = QPushButton('Back')
		back_button.setFont(QFont('Arial', 20))
		back_button.KEY_CHAR = Qt.Key_Backspace
		self.layout.addWidget(back_button, 5, 9, 1, 2)
		back_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
		back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


		# Done button
		done_button = QPushButton('Done')
		done_button.setFont(QFont('Arial', 20))
		done_button.KEY_CHAR = Qt.Key_Home
		self.layout.addWidget(done_button, 5, 11, 1, 2)
		done_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
		done_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.setLayout(self.layout)


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
			row, col, rowspan, colspan = self.layout.getItemPosition(i+1)
			self.layout.itemAtPosition(row, col).widget().setText(names[i])
			self.layout.itemAtPosition(row, col).widget().KEY_CHAR = ord(names[i])
			self.signalMapper.setMapping(self.layout.itemAtPosition(row, col).widget(), self.layout.itemAtPosition(row, col).widget().KEY_CHAR)

			

	def buttonClicked(self, char_ord):

		txt = self.text_box.text()

		if char_ord == Qt.Key_Backspace:
			txt = txt[:-1]
		elif char_ord == Qt.Key_Home:
			self.parent.ui.nameInput.setText(txt)
			self.parent.ui.nameInput.deselect()
			self.hide()
			return
		elif char_ord == Qt.Key_Shift:
			self.convertLetters()
		elif char_ord == Qt.Key_Space:
			txt += ' '
		elif char_ord == Qt.Key_Cancel:
			self.hide()
		else:
			txt += chr(char_ord)

		self.text_box.setText(txt)
