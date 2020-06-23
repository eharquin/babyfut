#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *

from ..core.module import Module
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent, QSignalMapper, QRect
from PyQt5.QtGui import QFont, QPainter

from ..core.database import Database
from ..core.tournament import Tournament, TournamentStatus, TournamentType
from ..core.team import Team, ConstructTeam
from ..core.player import Player

from .. import modules
from ..ui.authleague_ui import Ui_Form as TournamentWidget
from ..ui.create_tournament_dialog_ui import Ui_Dialog as CreateTournamentDialog
from ..ui.tournamentlist_ui import Ui_Form as TournamentListWidget
from ..ui.tournamentparticipant_ui import Ui_Form as TournamentParticipantWidget
from ..ui.tournamentdisplay_ui import Ui_Form as TournamentDisplayWidget
from ..ui.keyboard import KeyboardWidget
from ..ui.tournamentmatchlist_ui import Ui_Form as TournamentMatchWidget



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
		if e.key() == Qt.Key_Return:
			self.selectTn()


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
		self.ui.tournamentList.setCurrentRow(0)

	def selectTn(self):
		tn = self.ui.tournamentList.itemWidget(self.ui.tournamentList.currentItem()).tournament
		if tn.status==TournamentStatus.Future:
			# Display player list
			self.send(modules.TournamentParticipantModule, tournament = tn)
			self.switchModule(modules.TournamentParticipantModule)
		if tn.status==TournamentStatus.Running:
			self.send(modules.TournamentDisplayModule, tournament = tn)
			self.switchModule(modules.TournamentDisplayModule)
			
		if tn.status==TournamentStatus.Past:
			self.send(modules.TournamentDisplayModule, tournament = tn)
			self.switchModule(modules.TournamentDisplayModule)

'''
This class allows to show the tournament details. It can be launched only for tournaments with
status 'Future'. Teams can be added to the tournament, using the RFID readers.
Delete button and QListWidgetItem are to handle properly.
'''
class TournamentParticipantModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentParticipantWidget())
		self.parent = parent
		self.ui.btnAddTeam.clicked.connect(self.registerTeam)
		self.ui.btnStartTn.clicked.connect(self.startTournament)

	def load(self):
		logging.debug('Loading TournamentParticipantodule')
		self.ui.tnName.setText(self.tournament.name)
		self.ui.tnType.setText(self.ui.tnType.text().format(self.tournament.type.name))
		# Disable widget to add team unless rfid is received
		self.ui.teamName.setVisible(False)
		self.ui.photo1.setVisible(False)
		self.ui.photo2.setVisible(False)
		self.ui.fname1.setVisible(False)
		self.ui.fname2.setVisible(False)
		self.ui.btnAddTeam.setVisible(False)
		self.team = ConstructTeam(self)
		self.displayTeams()

	def unload(self):
		logging.debug('Unloading TournamentParticipantModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.TournamentModule)

	def other(self, **kwargs):
		logging.debug('Other TournamentParticipantModule')

		for key, val in kwargs.items():
			if key=='tournament':
				self.tournament = val

			if key=='rfid':
				self.addPlayer(val)

	def displayTeams(self):
		self.ui.teamList.clear()
		self.ui.teamList.setStyleSheet("color: rgb(64, 63, 63);font: bold 20px;border-width: 20px;")
		for team in self.tournament.teams:
			item = QListWidgetItem(team.name)
			self.ui.teamList.addItem(item)


	def addPlayer(self, rfid):
		player = Player.fromRFID(rfid)
		if (player!=Player.playerGuest()) and isinstance(self.team, ConstructTeam):
			if all(not team.hasPlayer(player) for team  in self.tournament.teams) and not self.team.hasPlayer(player):
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
		self.displayTeams()
		# Disable all team identification widgets
		self.ui.teamName.setVisible(False)
		self.ui.photo1.setVisible(False)
		self.ui.photo2.setVisible(False)
		self.ui.fname1.setVisible(False)
		self.ui.fname2.setVisible(False)
		self.ui.btnAddTeam.setVisible(False)
		self.team = ConstructTeam(self)

	def startTournament(self):
		self.tournament.validate()
		self.send(modules.TournamentDisplayModule, tournament = self.tournament)
		self.switchModule(modules.TournamentDisplayModule)


class TournamentDisplayModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentDisplayWidget())
		self.ui.matchList.itemDoubleClicked.connect(self.launchMatch)

	def load(self):
		logging.debug('Loading TournamentDisplayModule')
		self.ui.tnName.setText(self.tournament.name)
		#self.drawMatchTree()
		self.loadMatchList()

	def other(self, **kwargs):
		logging.debug('Other EndGameModule')

		for key, val in kwargs.items():
			if key=='tournament':
				self.tournament = val

	def unload(self):
		logging.debug('Unloading TournamentDisplayModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.TournamentModule)

	def drawMatchTree(self):
		self.tree = TreeMatch(self.tournament, self.ui.paintArea)
		self.ui.paintArea.addWidget(self.tree)

	def loadMatchList(self):
		self.ui.matchList.clear()
		print(self.tournament.currentRound)
		for round, liste in self.tournament.rounds.items():
			item=QListWidgetItem(str(round), self.ui.matchList)
			item.setFont(QFont('Ubuntu', 18))
			item.setTextAlignment(Qt.AlignCenter)
			item.setFlags(Qt.NoItemFlags)
			for match in liste:
				widget = QWidget()
				widget.setProperty("match", match)
				ui=TournamentMatchWidget()
				ui.setupUi(widget)
				t1 = match.teams[0].name if match.teams[0]!=None else "Winner of "+str(match.parents[0].id)
				ui.leftTeam.setText(t1)
				t2 = match.teams[1].name if match.teams[1]!=None else "Winner of "+str(match.parents[1].id)
				ui.rightTeam.setText(t2)
				ui.id.setText(str(match.id))
				if match.played==True:
					ui.leftScore.setText(str(match.scores[0]))
					ui.rightScore.setText(str(match.scores[1]))
				else:
					ui.leftScore.setText("")
					ui.rightScore.setText("")

				if match.playable() == True:
					widget.setStyleSheet('color : rgb(0,200,0)')
				else:
					widget.setStyleSheet('color : rgb(0,0,0)')

				
				item=QListWidgetItem(self.ui.matchList)
				
				item.setSizeHint(widget.size())
				self.ui.matchList.addItem(item)
				self.ui.matchList.setItemWidget(item, widget)

	def launchMatch(self):
		match = self.ui.matchList.itemWidget(self.ui.matchList.currentItem()).property("match")
		if match.playable() and not match.played:
			self.send(modules.GameModule, match=match)
			self.switchModule(modules.GameModule)


'''
Class that defines the TreeMatch view.
It inherits from a QWidget and reimplement the paintEvent function that draws the tree.
Unfinished...
'''
class TreeMatch(QWidget):
	def __init__(self, tournament, parent):
		super().__init__()
		self.tournament = tournament
		self.parent = parent

	def paintEvent(self, event):
		#self.parent.clear()
		painter = QPainter(self)
		j=1
		for round, liste in self.tournament.rounds.items():
			i=1
			for match in liste:
				painter.drawRect((self.width()/(len(liste)+1))*i,100*j,50,50)
				i+=1
			j+=1


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
		