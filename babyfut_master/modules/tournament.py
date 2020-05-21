#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *

from ..core.module import Module
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent, QSignalMapper
from PyQt5.QtGui import QFont

from ..core.database import Database
from ..core.tournament import Tournament, TournamentStatus, TournamentType
from ..core.team import Team, ConstructTeam
from ..core.player import Player

from .. import modules
from ..ui.authleague_ui import Ui_Form as TournamentWidget
from ..ui.create_tournament_dialog_ui import Ui_Dialog as CreateTournamentDialog
from ..ui.tournamentlist_ui import Ui_Form as TournamentListWidget
from ..ui.tournamentparticipant_ui import Ui_Form as TournamentParticipantWidget
from ..ui.keyboard import KeyboardWidget



class TournamentListItem(QWidget):
	def __init__(self, parent, tournament):
		QWidget.__init__(self, parent)
		self.tournament = tournament
		self.ui = TournamentListWidget()
		self.ui.setupUi(self)
		self.ui.tnName.setText(tournament.name)
		self.ui.tnStatus.setText(self.ui.tnStatus.text().format(tournament.status.name))
		self.ui.tnType.setText(self.ui.tnType.text().format(tournament.type.name))
		self.ui.btnDelete.clicked.connect(self.deleteTn)

	def deleteTn(self):
		# Need to print a QDialog and then delete
		pass


class TournamentModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentWidget())
		self.parent = parent
		self.ui.btnCreate.clicked.connect(self.createTournament)
		self.ui.btnGo.clicked.connect(self.selectTn)

	def load(self):
		logging.debug('Loading TournamentModule')
		self.loadTournaments()

	def unload(self):
		logging.debug('Loading TournamentModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.MenuModule)

	def createTournament(self):
		dialog = CreateDialog(self)
		dialog.exec()

	def loadTournaments(self):
		self.ui.tournamentList.clear()
		tournaments = Tournament.selectAll()
		for tournament in tournaments:
			item = QListWidgetItem()
			tnWidget = TournamentListItem(self.ui.tournamentList,tournament)
			item.setSizeHint(tnWidget.size())
			self.ui.tournamentList.addItem(item)
			self.ui.tournamentList.setItemWidget(item, tnWidget)

	def selectTn(self):
		tn = self.ui.tournamentList.itemWidget(self.ui.tournamentList.currentItem()).tournament
		if tn.status==TournamentStatus.Future:
			# Display player list
			self.send(modules.TournamentParticipantModule, tournament = tn)
			self.switchModule(modules.TournamentParticipantModule)
			pass
		if tn.status==TournamentStatus.Running:
			# Display tournament
			pass
		if tn.status==TournamentStatus.Passed:
			# Display tournament table and results
			pass

class TournamentParticipantModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentParticipantWidget())
		self.parent = parent
		self.ui.btnAddTeam.clicked.connect(self.registerTeam)

	def load(self):
		logging.debug('Loading TournamentParticipantodule')
		self.ui.tnName.setText(self.tournament.name)
		self.ui.tnType.setText(self.ui.tnType.text().format(self.tournament.type.name))
		self.ui.teamName.setVisible(False)
		self.ui.photo1.setVisible(False)
		self.ui.photo2.setVisible(False)
		self.ui.fname1.setVisible(False)
		self.ui.fname2.setVisible(False)
		self.ui.btnAddTeam.setVisible(False)
		self.team = ConstructTeam(self)
		self.displayTeams()

	def unload(self):
		logging.debug('Loading TournamentParticipantModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.TournamentModule)

	def other(self, **kwargs):
		logging.debug('Other EndGameModule')

		for key, val in kwargs.items():
			if key=='tournament':
				self.tournament = val

			if key=='rfid':
				self.addPlayer(val)

	def displayTeams(self):
		for team in self.tournament.teams:
			item = QListWidgetItem(team.name)
			self.ui.teamList.addItem(item)


	def addPlayer(self, rfid):
		player = Player.fromRFID(rfid)
		self.team = self.team.addPlayer(player)
		if self.team.size()==1:
			self.ui.btnAddTeam.setVisible(True)
			player.displayImg(self.ui.photo1)
			self.ui.photo1.setVisible(True)
			self.ui.fname1.setText(player.name)
			self.ui.fname1.setVisible(True)
		else:
			player.displayImg(self.ui.photo2)
			self.ui.photo2.setVisible(True)
			self.ui.fname2.setText(player.name)
			self.ui.fname2.setVisible(True)
			self.ui.teamName.setText(self.team.name)
			self.ui.teamName.setVisible(True)

	def registerTeam(self):
		if isinstance(self.team, ConstructTeam):
			self.team = self.team.validateTeam()
		self.tournament.registerTeam(self.team)



class CreateDialog(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.parent=parent
		self.ui = CreateTournamentDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Create a tournament')
		self.keyboard = KeyboardWidget(self, "Enter the tournament's name")
		self.keyboard.hide()
		
		self.ui.editName.clicked.connect(self.keyboard.show)
		self.ui.enter.clicked.connect(lambda : self.createTournament(self.ui.nameInput.text(), self.ui.typeTn.currentIndex()))

	def keyboardResult(self, texte=None):
		if texte:
			self.ui.nameInput.setText(texte)

	# May handle other options in the future
	def createTournament(self, name, typeTn):
		tn = Tournament.create(name, TournamentType(typeTn))
		self.parent.send(modules.TournamentParticipantModule, tournament = tn)
		self.parent.switchModule(modules.TournamentParticipantModule)
		self.finish()

	def finish(self):
		self.done(1)
		