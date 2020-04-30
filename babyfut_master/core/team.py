#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging
# from math import sqrt
# from http import HTTPStatus

from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QDialog, QApplication

from ..babyfut_master import getMainWin, IMG_PATH
from .player import Player
# from .ginger import Ginger, GingerError
from .database import Database, DatabaseError
# from ..ui.consent_dialog_ui import Ui_Dialog as ConsentDialogUI


class Team(QObject):

    def __init__(self):
        self.players=list()
        self.players.append(Player.playerGuest())
        self.name = None
        self.id = None

    def setName(self, name):
        if self.size()==2:
            self.name = name

    def size(self):
        return len(self.players)

    def addPlayer(self, player):
        if player==Player.playerGuest():
            return

        if Player.playerGuest() in self.players:
            self.players.remove(Player.playerGuest())
        
        if len(self.players)<2:
            self.players.append(player)

    def insertDB(self):
        db = Database.instance()
        if not self.exists():
            if len(self.players)==2:
                db.insertTeam(self.name, self.players[0].login, self.players[1].login)
            if len(self.players)==1:
                db.insertTeam(self.name, self.players[0].login)

    def exists(self):
        if not Player.playerGuest() in self.players:
            try:
                if len(self.players)==2:
                    result = Database.instance().checkTeam(self.players[0].login, self.players[1].login)
                elif len(self.players)==1:
                    result = Database.instance().checkTeam(self.players[0].login)
                self.id=result[0]
                self.name = result[1]
                return True
            except:
                return False
        else:
            return True

    def isPlayer(self, player):
        if any(p.login == player.login for p in self.players):
            return True
        else:
            return False

