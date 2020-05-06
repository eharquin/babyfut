#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend
"""

import logging

from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QWidget, QListWidgetItem

from ..core.player import Player
from ..core.module import Module
from .. import modules
from ..ui.edit_ui import Ui_Form as EditWidget
from ..ui.teamlist_ui import Ui_Form as TeamListWidget
from ..ui.gamelist_ui import Ui_Form as GameListWidget
from ..core.database import Database, DatabaseError


class TeamListItem(QWidget):
    def __init__(self, parent, team, teamMate):
        QWidget.__init__(self, parent)
        self.ui = TeamListWidget()
        self.ui.setupUi(self)
        self.teamID = team[0]
        self.setFixedWidth(parent.width()-parent.verticalScrollBar().width())

        self.ui.teamName.setText(team[1])
        self.ui.teamMate.setText(self.ui.teamMate.text().format(teamMate[1]+' '+teamMate[2]))


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
                self.ui.mainLayout.setVisible(True)
                self.ui.subtitle.setVisible(False)


    def loadPlayer(self, rfid):
        # Get player
        self.player = Player.fromRFID(rfid)
        
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
    
    
    def loadTeams(self):
        self.ui.teamList.clear()
        teams = Database.instance().selectPlayerTeams(self.player.login)

        for team in teams:
            teamMate = Database.instance().selectPlayer(team[2])
            item = QListWidgetItem()
            teamWidget = TeamListItem(self.ui.teamList, team, teamMate)
            item.setSizeHint(teamWidget.size())
            teamWidget.ui.editButton.clicked.connect(self.editTeamName)
            self.ui.teamList.addItem(item)
            self.ui.teamList.setItemWidget(item, teamWidget)
            self.ui.teamList.setStyleSheet("color: rgb(63, 63, 63)")


    def loadGames(self):
        pass

    # Open a QDialog (same as authquick with team name and keyboard)
    def editTeamName(self):
        pass

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
        self.switchModule(modules.MenuModule)
