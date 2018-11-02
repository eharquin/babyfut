#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
from operator import attrgetter

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, Qt, QSize, QItemSelectionModel

from module import Module
import modules
from player import PlayerGuest, Player
from ui.leaderboard_ui import Ui_Form as LeaderboardWidget
from ui.playerlist_ui import Ui_Form as PlayerListWidget

class LeaderboardItemWidget(QtWidgets.QWidget):
	def __init__(self, parent, player):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = PlayerListWidget()
		self.ui.setupUi(self)
		
		player.displayImg(self.ui.picHolder)
		self.ui.lblFName.setText(player.fname)
		self.ui.lblLName.setText(player.lname)
		
		self.ui.lblVictories.setText    (self.ui.lblVictories.text().replace('####',     str(player.stats['victories'])))
		self.ui.lblGamesPlayed.setText  (self.ui.lblGamesPlayed.text().replace('####',   str(player.stats['games_played'])))
		self.ui.lblGoalsScored.setText  (self.ui.lblGoalsScored.text().replace('####',   str(player.stats['goals_scored'])))
		self.ui.lblMinutesPlayed.setText(self.ui.lblMinutesPlayed.text().replace('####', str(player.stats['time_played'])))
		
		self.ui.pushButton.clicked.connect(lambda: logging.debug('clicked'))

class LeaderboardModule(Module):
	def __init__(self, parent):
		super().__init__(parent, LeaderboardWidget())
		self.players = []
		
		self.ui.rbName.clicked.connect(lambda: self.changeSort(self.ui.rbName))
		self.ui.rbVictories.clicked.connect(lambda: self.changeSort(self.ui.rbVictories))
		self.ui.rbScore.clicked.connect(lambda: self.changeSort(self.ui.rbScore))
		self.ui.rbGamesPlayed.clicked.connect(lambda: self.changeSort(self.ui.rbGamesPlayed))
		self.ui.rbTimePlayed.clicked.connect(lambda: self.changeSort(self.ui.rbTimePlayed))
		
		self.selectedSort = 0
		self.sortMethodRB = [self.ui.rbName, self.ui.rbVictories, self.ui.rbScore, self.ui.rbGamesPlayed, self.ui.rbTimePlayed]
		self.sortMethodAttr = ['lname', 'stats_property.victories', 'stats_property.goals_scored', 'stats_property.games_played', 'stats_property.time_played']
		
		self.sortMethodRB[self.selectedSort].setChecked(True)

	def load(self):
		logging.debug('Loading LeaderboardModule')
		self.loadList()
		self.setFocus()

	def unload(self):
		logging.debug('Unloading LeaderboardModule')
		self.players = []

	def other(self, **kwargs):
		logging.debug('Other LeaderboardModule')
	
	def changeSort(self, rbSort):
		self.selectedSort = self.sortMethodRB.index(rbSort)
		self.loadList()
	
	def loadList(self):
		if self.players:
			self.ui.listWidget.clear()
		else:
			self.players = [Player.fromRFID(id) for id in range(-2 , -7, -1)]
		
		self.players.sort(key=attrgetter(self.sortMethodAttr[self.selectedSort]), reverse=True)
		
		for player in self.players:
			item = QtWidgets.QListWidgetItem()
			playerWidget = LeaderboardItemWidget(self.ui.listWidget, player)
			item.setSizeHint(playerWidget.size())
			self.ui.listWidget.addItem(item)
			self.ui.listWidget.setItemWidget(item, playerWidget)
		
		self.ui.listWidget.setCurrentRow(0, QItemSelectionModel.Select)

	def keyPressEvent(self, e):
		curRow = self.ui.listWidget.currentRow()
		curSort = self.selectedSort
		
		if e.key() == Qt.Key_Escape:
			self.handleExit()
			
		elif e.key() == Qt.Key_Up:
			newRow = curRow-1 if curRow!=0 else self.ui.listWidget.count()-1
			self.ui.listWidget.setCurrentRow(newRow, QItemSelectionModel.SelectCurrent)
			
		elif e.key() == Qt.Key_Down:
			newRow = curRow+1 if curRow!=self.ui.listWidget.count()-1 else 0
			self.ui.listWidget.setCurrentRow(newRow, QItemSelectionModel.SelectCurrent)
			
		elif e.key() == Qt.Key_Left:
			newSort = curSort-1 if curSort!=0 else len(self.sortMethodRB)-1
			self.sortMethodRB[newSort].animateClick()
			
		elif e.key() == Qt.Key_Right:
			newSort = curSort+1 if curSort!=len(self.sortMethodRB)-1 else 0
			self.sortMethodRB[newSort].animateClick()

	def handleExit(self):
		self.switchModule(modules.MenuModule)
