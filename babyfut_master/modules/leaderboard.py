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

		player.displayImg(self.ui.picHolder)
		self.ui.lblFName.setText(player.fname)
		self.ui.lblLName.setText(player.lname)

		self.ui.lblVictories.setText    (self.ui.lblVictories.text().format(player.stats.victories     ))
		self.ui.lblGamesPlayed.setText  (self.ui.lblGamesPlayed.text().format(player.stats.games_played  ))
		self.ui.lblGoalsScored.setText  (self.ui.lblGoalsScored.text().format(player.stats.goals_scored  ))
		self.ui.lblMinutesPlayed.setText(self.ui.lblMinutesPlayed.text().replace('{}', '{0:.2f}').format(player.stats.time_played/60))
		self.ui.lblElo.setText  (self.ui.lblElo.text().format(player.eloRating))
		self.ui.lblRatio.setText(self.ui.lblRatio.text().replace('{}', '{:.2f}').format(player.stats.ratioIndex))


class DeleteDialog(QDialog):
	class Actions(Enum):
		DeleteAll     = 0
		DeletePicture = 1
		HideAccount   = 2

	def __init__(self, parent, player):
		QDialog.__init__(self, parent)
		self.ui = PlayerDeleteDialog()
		self.ui.setupUi(self)
		self.player = player
		self.ui.lblTitle.setText(self.ui.lblTitle.text().format(player.name))
		self.setWindowTitle('Data account manager')

	def check(self, rfid):
		return rfid == self.player.rfid

	def action(self):
		dict_actions = {
			self.ui.rbDeleteAll:     DeleteDialog.Actions.DeleteAll,
			self.ui.rbDeletePicture: DeleteDialog.Actions.DeletePicture,
			self.ui.rbHideAccount:   DeleteDialog.Actions.HideAccount
		}

		for key, val in dict_actions.items():
			if key.isChecked():
				return val
		return None

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Return:
			# Debug
			self.parent().send(modules.LeaderboardModule, rfid=self.player.rfid, source=Side.Right)
		elif e.key() == Qt.Key_Escape:
			self.reject()

class LeaderboardModule(Module):
	def __init__(self, parent):
		super().__init__(parent, LeaderboardWidget())
		self.players = []

		self.ui.rbRatio.clicked.connect(lambda: self.changeSort(self.ui.rbRatio))
		self.ui.rbElo.clicked.connect(lambda: self.changeSort(self.ui.rbElo))
		self.ui.rbName.clicked.connect(lambda: self.changeSort(self.ui.rbName))
		self.ui.rbVictories.clicked.connect(lambda: self.changeSort(self.ui.rbVictories))
		self.ui.rbScore.clicked.connect(lambda: self.changeSort(self.ui.rbScore))
		self.ui.rbGamesPlayed.clicked.connect(lambda: self.changeSort(self.ui.rbGamesPlayed))
		self.ui.rbTimePlayed.clicked.connect(lambda: self.changeSort(self.ui.rbTimePlayed))

		self.selectedSort = 0
		self.sortMethodRB = [self.ui.rbRatio, self.ui.rbElo, self.ui.rbName, self.ui.rbVictories, self.ui.rbScore, self.ui.rbGamesPlayed, self.ui.rbTimePlayed]
		self.sortMethodAttr = ['stats.ratioIndex','eloRating', 'lname', 'stats.victories', 'stats.goals_scored', 'stats.games_played', 'stats.time_played']

		self.sortMethodRB[self.selectedSort].setChecked(True)
		self.deleteDialog = None

	def load(self):
		logging.debug('Loading LeaderboardModule')
		self.selectedSort = 0
		self.loadList()
		self.setFocus()

	def unload(self):
		logging.debug('Unloading LeaderboardModule')
		self.players = []
		self.ui.listWidget.clear()

	def other(self, **kwargs):
		logging.debug('Other LeaderboardModule')

		for key, val in kwargs.items():
			if key=='rfid' and self.deleteDialog and self.deleteDialog.check(val):
				# Do something corresponding to the selected action
				action = self.deleteDialog.action()
				if action==DeleteDialog.Actions.DeleteAll:
					#Database.instance().delete_player(self.deleteDialog.player.id)
					print("Deleted")
				elif action==DeleteDialog.Actions.DeletePicture:
					self.deleteDialog.player.forgetPicture()
				elif action==DeleteDialog.Actions.HideAccount:
					self.deleteDialog.player.makePrivate()
				else:
					logging.error('Unknown action {}'.format(action))

				# Reset the dialog and the player list
				self.deleteDialog.close()
				del self.deleteDialog
				self.deleteDialog = None
				self.players = []
				self.ui.listWidget.clear()
				self.loadList()
			elif key=='rfid':
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
		self.loadList()

	def loadList(self):
		if self.players:
			self.ui.listWidget.clear()
		else:
			self.players = Player.allStoredPlayers()

		self.players.sort(key=attrgetter(self.sortMethodAttr[self.selectedSort]), reverse=(self.sortMethodAttr[self.selectedSort]!='lname'))

		for player in self.players:
			item = QListWidgetItem()
			#data = Player._loadFromDB(player.login)
			playerWidget = LeaderboardItemWidget(self.ui.listWidget, player)
			#row = self.ui.listWidget.count()-1
			playerWidget.ui.deleteButton.clicked.connect(lambda:self.deletePlayer(None))
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

		elif e.key() == Qt.Key_Delete:
			self.deletePlayer(curRow)
			
	def deletePlayer(self, row=None):
		if row==None:
			for num in range(0, self.ui.listWidget.count()):
				if self.ui.listWidget.itemWidget(self.ui.listWidget.item(num))==self.sender().parent():
					row = num
		self.ui.listWidget.setFocus()
		self.deleteDialog = DeleteDialog(self, self.players[row])
		self.deleteDialog.open()

	def handleExit(self):
		self.switchModule(modules.MenuModule)
