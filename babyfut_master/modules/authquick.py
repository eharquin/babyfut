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
from ..core.team import Team
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
		self.updateSides(Side.Left)
		self.updateSides(Side.Right)
		
		self.ui.lblStarting.setVisible(False)
		
	def unload(self):
		logging.debug('Unloading AuthQuickModule')
		super().unload()

	def createTeamList(self):
		self.teams = {Side.Left: Team(), Side.Right: Team()}

	def _timerHandler(self):
		self.timerCount = self.timerCount -1
		self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
		if self.timerCount<=0:
			self.startingGameTimer.stop()
			self.handleDone()
		
	def addPlayer(self, side, player):
		if self.teams[side].size()<2:
			self.teams[side].addPlayer(player)
			self.updateSides(side)
			if self.teams[side].size()==2:
				if not self.teams[side].exists():
					self.getTeamName = TeamName(self, self.teams[side])
					self.getTeamName.exec()

				if self.teams[side.opposite()]==2:
					self.timerCount = 5
					self.ui.lblStarting.setText('Starting in {}...'.format(self.timerCount))
					self.ui.lblStarting.setVisible(True)
					self.startingGameTimer.start(1000)
			self.changeTeamName(side)
		

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


class TeamName(QDialog):
	def __init__(self, parent, team):
		QDialog.__init__(self, parent)
		self.parent = parent
		self.team = team
		self.ui = TeamNameDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Create a team')
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(team.players[0].fname, team.players[1].fname))
		self.ui.nameInput.setText(self.setRandomName())
		self.ui.nameInput.setReadOnly(True)
		self.keyboard = KeyboardWidget(self)
		self.keyboard.hide()
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
	def __init__(self, parent=None):
		super(KeyboardWidget, self).__init__(parent)
		self.parent = parent
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

		self.verticalLayout.addWidget(self.text_box)

		self.maj = True
		self.namesMaj = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
						'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
						'Q', 'S', 'D','F', 'G', 'H', 'J', 'K', 'L', 'M', 
						'W', 'X', 'C', 'V', 'B', 'N', '?', '!', '.', '-']
		
		self.namesMin =  ['é', 'è', 'à', 'ç', '(', ')', '[', ']', '_', '@',
						'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
						'q', 's', 'd','f', 'g', 'h', 'j', 'k', 'l', 'm',
						'w', 'x', 'c', 'v', 'b', 'n',',',';',':','/']

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
		elif char_ord == Qt.Key_Home:
			self.parent.ui.nameInput.setText(txt)
			self.parent.ui.nameInput.setFocusPolicy(Qt.NoFocus)
			self.parent.setFocus()
			self.parent.ui.enter.setDefault(True)
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

		self.setFocus()
		self.text_box.setText(txt)
