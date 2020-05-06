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
        self._name = None
        
        #ID null means Team not related to Database (Guest, waiting for player)
        self.id = None

    def setName(self, name):
        if self.size()==2:
            self._name = name

    @property
    def name(self):
        if self.size()==2:
            return self._name
        else:
            return self.players[0].name

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
                if not self._name:
                    self._name='2 Players Team'
                self.id = db.insertTeam(self.players[0].login, self.players[1].login, self._name)
            if len(self.players)==1:
                self._name=None
                self.id = db.insertTeam(self.players[0].login)

    def exists(self):
        if Player.playerGuest() in self.players:
            return True
        else:
            try:
                logins = [p.login for p in self.players]
                result = Database.instance().checkTeam(*logins)
                if result:
                    self.id=result[0]
                    self._name = result[1]
                    return True
                else:
                    return False
            except DatabaseError as e:
                logging.error('DatabaseError : {}'.format(e))
                return False


    def hasPlayer(self, player):
        if any(p.login == player.login for p in self.players):
            return True
        else:
            return False
    
    def hasGuest(self):
        return self.hasPlayer(Player.playerGuest())
