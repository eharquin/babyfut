#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import logging, time
from datetime import datetime

from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QWidget, QListWidgetItem

from ..core.player import Player
from ..core.module import Module
from ..ui.edit_ui import Ui_Form as EditWidget
from ..ui.teamlist_ui import Ui_Form as TeamListWidget
from ..ui.gamelist_ui import Ui_Form as GameListWidget
from ..core.database import Database, DatabaseError
from ..core.team import Team
from common.module_switch import EditSwitch

class TeamListItem(QWidget):
    def __init__(self, parent, currentPlayer, team):
        QWidget.__init__(self, parent)
        self.ui = TeamListWidget()
        self.ui.setupUi(self)
        self.team = team
        self.parent = parent
        self.setFixedWidth(parent.width()-20)

        self.ui.teamName.setText(self.team.name)
        if self.team.players[0].login == currentPlayer:
            self.ui.teamMate.setText(self.ui.teamMate.text().format(self.team.players[1].name))
        elif self.team.players[1].login == currentPlayer:
            self.ui.teamMate.setText(self.ui.teamMate.text().format(self.team.players[0].name))

        self.ui.editButton.clicked.connect(self.changeTeamName)

    def changeTeamName(self):
        self.team.getNameDialog(self.parent.parent())
        self.ui.teamName.setText(self.team.name)

class GameListItem(QWidget):
    def __init__(self, parent, currentPlayer, game):
        QWidget.__init__(self, parent)
        self.ui = GameListWidget()
        self.ui.setupUi(self)
        self.setFixedWidth(parent.width()-20)

        self.ui.gameDate.setText(str(datetime.fromtimestamp(game[0]).strftime("%d/%m/%y")))

        # Game is like (matchID, team1, score1, team2, score2, winningTeamID)
        team1 = Team.loadFromDB(game[1])
        team2 = Team.loadFromDB(game[3])

        self.ui.picture.setStyleSheet('border-image: url(:/ui/img/icons/lost.png)')
        self.ui.leftTeam.setText(team1.name)
        self.ui.leftScore.setText(str(game[2]))
        self.ui.rightScore.setText(str(game[4]))
        self.ui.rightTeam.setText(team2.name)

        basefont = self.ui.leftTeam.font()
        basefont.setBold(True)
        if team1.hasPlayer(currentPlayer):
            self.ui.leftTeam.setFont(basefont)
            if team1.id==game[5]:
                self.ui.picture.setStyleSheet('border-image: url(:/ui/img/icons/won.jpg)')
        else:
            self.ui.rightTeam.setFont(basefont)
            if team2.id==game[5]:
                self.ui.picture.setStyleSheet('border-image: url(:/ui/img/icons/won.jpg)')
        # If equality between teams
        if game[5]==-1:
            self.ui.picture.setStyleSheet('border-image: url(:/ui/img/icons/equal.png)')


class EditModule(Module):
    def __init__(self, parent):
        super().__init__(parent, EditWidget())
        self.ui.deleteAccount.clicked.connect(self.deleteAccount)
        self.ui.privateYes.clicked.connect(lambda: self.makePrivate(True))
        self.ui.privateNo.clicked.connect(lambda: self.makePrivate(False))
        self.ui.editPhoto.clicked.connect(self.editPlayerPhoto)


    def load(self):
        logging.debug('Loading EditModule')
        self.ui.mainLayout.setVisible(False)
        self.ui.subtitle.setVisible(True)
        self.setFocus()


    def unload(self):
        logging.debug('Unloading OptionsModule')


    def other(self, **kwargs):
        logging.debug('Other EditModule')

        for key, val in kwargs.items():
            if key=='rfid':
                self.loadPlayer(val)


    def loadPlayer(self, rfid):
        # Get player
        self.player = Player.fromRFID(rfid)
        if self.player != Player.playerGuest():
            self.ui.mainLayout.setVisible(True)
            self.ui.subtitle.setVisible(False)
            # Set all widget with player info
            self.player.displayImg(self.ui.playerPhoto)
            self.ui.fname.setText(self.player.fname)
            self.ui.lname.setText(self.player.lname)

            # Set radioButton to the current position
            if self.player.private:
                self.ui.privateYes.setChecked(True)
            else:
                self.ui.privateNo.setChecked(True)

            self.loadTeams()
            self.loadGames()
        else:
            logging.debug("Unknown player")


    def loadTeams(self):
        self.ui.teamList.clear()
        teams = Database.instance().selectPlayerTeams(self.player.login)

        for team in teams:
            item = QListWidgetItem()
            player1 = Player.loadFromDB(team[2])
            player2 = Player.loadFromDB(team[3])
            teamWidget = TeamListItem(self.ui.teamList, self.player.login, Team(team[0], team[1], [player1, player2]))
            item.setSizeHint(teamWidget.size())
            self.ui.teamList.addItem(item)
            self.ui.teamList.setItemWidget(item, teamWidget)


    def loadGames(self):
        self.ui.gameList.clear()
        games = Database.instance().selectPlayerGames(self.player.login)
        print(games)
        for game in games:
            item = QListWidgetItem()
            gameWidget = GameListItem(self.ui.gameList, self.player, game)
            item.setSizeHint(gameWidget.size())
            self.ui.gameList.addItem(item)
            self.ui.gameList.setItemWidget(item, gameWidget)

    def makePrivate(self, option):
            self.player.makePrivate(option)

    def editPlayerPhoto(self):
        self.deleteWarning = QMessageBox(self)
        self.deleteWarning.setStyleSheet("color: black")
        self.deleteWarning.setWindowTitle('WIP')
        self.deleteWarning.setText('Changing your picture will be available soon!')
        self.deleteWarning.setStandardButtons(QMessageBox.Ok)
        choice = self.deleteWarning.exec()


    def deleteAccount(self):
        self.deleteWarning = QMessageBox(self)
        self.deleteWarning.setStyleSheet("color: black")
        self.deleteWarning.setWindowTitle('Delete your account?')
        self.deleteWarning.setText('Warning! You are about to delete all your records. Are you sure you want to do it?')
        self.deleteWarning.setStandardButtons(QMessageBox.Ok)
        self.deleteWarning.addButton(QMessageBox.Cancel)
        choice = self.deleteWarning.exec()
        if choice==QMessageBox.Ok:
            self.player.deletePlayer()
            self.handleBack()
        else:
            logging.debug("Cancel player deletion")


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.handleBack()
        elif e.key() == Qt.Key_Return:
            self.handleBack()


    def handleBack(self):
        EditSwitch(self).back()
