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

from Babyfut import modules
from Babyfut.core.module import Module
from Babyfut.core.player import Player, Side
from Babyfut.core.database import Database
from Babyfut.ui.leaderboard_ui import Ui_Form as LeaderboardWidget
from Babyfut.ui.playerlist_ui import Ui_Form as PlayerListWidget
from Babyfut.ui.delete_dialog_ui import Ui_Dialog as PlayerDeleteDialog

class LeaderboardItemWidget(QWidget):
	def __init__(self, parent, player):
		QWidget.__init__(self, parent)
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

	def check(self, rfid):
		return rfid == -self.player.id

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

		self.ui.rbName.clicked.connect(lambda: self.changeSort(self.ui.rbName))
		self.ui.rbVictories.clicked.connect(lambda: self.changeSort(self.ui.rbVictories))
		self.ui.rbScore.clicked.connect(lambda: self.changeSort(self.ui.rbScore))
		self.ui.rbGamesPlayed.clicked.connect(lambda: self.changeSort(self.ui.rbGamesPlayed))
		self.ui.rbTimePlayed.clicked.connect(lambda: self.changeSort(self.ui.rbTimePlayed))

		self.selectedSort = 0
		self.sortMethodRB = [self.ui.rbName, self.ui.rbVictories, self.ui.rbScore, self.ui.rbGamesPlayed, self.ui.rbTimePlayed]
		self.sortMethodAttr = ['lname', 'stats_property.victories', 'stats_property.goals_scored', 'stats_property.games_played', 'stats_property.time_played']

		self.sortMethodRB[self.selectedSort].setChecked(True)
		self.deleteDialog = None

	def load(self):
		logging.debug('Loading LeaderboardModule')
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
					Database.instance().delete_player(self.deleteDialog.player.id)
				elif action==DeleteDialog.Actions.DeletePicture:
					logging.error('Unimplemented action: delete picture')
				elif action==DeleteDialog.Actions.HideAccount:
					logging.error('Unimplemented action: Hide account')
				else:
					logging.error('Unknown action {}'.format(action))

				# Reset the dialog and the player list
				self.deleteDialog.close()
				del self.deleteDialog
				self.deleteDialog = None
				self.players = []
				self.ui.listWidget.clear()
				self.loadList()

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

		elif e.key() == Qt.Key_Delete:
			self.deleteDialog = DeleteDialog(self, self.players[curRow])
			self.deleteDialog.open()

	def handleExit(self):
		self.switchModule(modules.MenuModule)
