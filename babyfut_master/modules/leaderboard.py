#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
from enum import Enum
from operator import attrgetter

from PyQt5.QtWidgets import QWidget, QDialog, QListWidgetItem
from PyQt5.QtCore import Qt, QItemSelectionModel

from .. import modules
from ..core.module import Module
from ..core.player import Player
from common.side import Side
from ..core.database import Database
from ..ui.leaderboard_ui import Ui_Form as LeaderboardWidget
from ..ui.playerlist_ui import Ui_Form as PlayerListWidget
from ..ui.delete_dialog_ui import Ui_Dialog as PlayerDeleteDialog

class LeaderboardItemWidget(QWidget):
	def __init__(self, parent, player):
		QWidget.__init__(self, parent)
		self.ui = PlayerListWidget()
		self.ui.setupUi(self)
		self.setFixedWidth(parent.width()-20)
		player.displayImg(self.ui.picHolder)
		self.ui.lblFName.setText(player.fname)
		self.ui.lblLName.setText(player.lname)

		self.ui.lblVictories.setText    (self.ui.lblVictories.text().format(player.stats.victories     ))
		self.ui.lblGamesPlayed.setText  (self.ui.lblGamesPlayed.text().format(player.stats.games_played  ))
		self.ui.lblGoalsScored.setText  (self.ui.lblGoalsScored.text().format(player.stats.goals_scored  ))
		self.ui.lblMinutesPlayed.setText(self.ui.lblMinutesPlayed.text().replace('{}', '{0:.2f}').format(player.stats.time_played/60))
		self.ui.lblElo.setText  (self.ui.lblElo.text().format(player.eloRating))
		self.ui.lblRatio.setText(self.ui.lblRatio.text().replace('{}', '{:.2f}').format(player.stats.ratioIndex))


class LeaderboardModule(Module):
	def __init__(self, parent):
		super().__init__(parent, LeaderboardWidget())
		self.players = []

		#Connecting Radio Button for sorting method
		self.ui.rbRatio.clicked.connect(lambda: self.changeSort(self.ui.rbRatio))
		self.ui.rbElo.clicked.connect(lambda: self.changeSort(self.ui.rbElo))
		self.ui.rbName.clicked.connect(lambda: self.changeSort(self.ui.rbName))
		self.ui.rbVictories.clicked.connect(lambda: self.changeSort(self.ui.rbVictories))
		self.ui.rbScore.clicked.connect(lambda: self.changeSort(self.ui.rbScore))
		self.ui.rbGamesPlayed.clicked.connect(lambda: self.changeSort(self.ui.rbGamesPlayed))
		self.ui.rbTimePlayed.clicked.connect(lambda: self.changeSort(self.ui.rbTimePlayed))

		self.sortMethodRB = [self.ui.rbRatio, self.ui.rbElo, self.ui.rbName, self.ui.rbVictories, self.ui.rbScore, self.ui.rbGamesPlayed, self.ui.rbTimePlayed]
		self.sortMethodAttr = ['stats.ratioIndex','eloRating', 'lname', 'stats.victories', 'stats.goals_scored', 'stats.games_played', 'stats.time_played']


	def load(self):
		logging.debug('Loading LeaderboardModule')
		self.players = Player.allStoredPlayers()
		self.selectedSort=0
		self.sortMethodRB[self.selectedSort].setChecked(True)
		self.changeSort(self.sortMethodRB[self.selectedSort])
		self.setFocus()

	def unload(self):
		logging.debug('Unloading LeaderboardModule')
		self.players = []
		self.ui.listWidget.clear()

	def other(self, **kwargs):
		logging.debug('Other LeaderboardModule')

		for key, val in kwargs.items():
			#Scrolling to the badger's line in QListView
			if key=='rfid':
				login = (Player.fromRFID(val)).login
				row=0
				for player in self.players:
					if player.login == login:
						self.ui.listWidget.setCurrentRow(row)
						break
					else:
						row+=1



	def changeSort(self, rbSort):
		self.selectedSort = self.sortMethodRB.index(rbSort)
		if self.sortMethodAttr[self.selectedSort]!='lname':
			self.players.sort(key=attrgetter(self.sortMethodAttr[self.selectedSort], 'stats.ratioIndex'), reverse=True)
		else:
			self.players.sort(key=attrgetter('lname', 'fname'))
		self.loadList()

	def loadList(self):
		self.ui.listWidget.clear()

		for player in self.players:
			item = QListWidgetItem()
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
			if curRow!=0:
				self.ui.listWidget.setCurrentRow(curRow-1, QItemSelectionModel.SelectCurrent)

		elif e.key() == Qt.Key_Down:
			if curRow!=self.ui.listWidget.count()-1:
				self.ui.listWidget.setCurrentRow(curRow+1, QItemSelectionModel.SelectCurrent)

		elif e.key() == Qt.Key_Left:
			newSort = curSort-1 if curSort!=0 else len(self.sortMethodRB)-1
			self.sortMethodRB[newSort].animateClick()

		elif e.key() == Qt.Key_Right:
			newSort = curSort+1 if curSort!=len(self.sortMethodRB)-1 else 0
			self.sortMethodRB[newSort].animateClick()


	def handleExit(self):
		self.switchModule(modules.MenuModule)
