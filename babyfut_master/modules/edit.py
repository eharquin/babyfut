#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QRadioButton, QMessageBox

from ..core.player import Player
from ..core.module import Module
from .. import modules
from ..ui.edit_ui import Ui_Form as EditWidget
from ..ui.teamlist_ui import Ui_Form as TeamListWidget
from ..ui.gamelist_ui import Ui_Form as GameListWidget


class EditModule(Module):
    def __init__(self, parent):
        super().__init__(parent, EditWidget())
        self.parent = parent
        self.ui.deleteAccount.clicked.connect(self.deleteAccount)
        self.ui.privateYes.clicked.connect(lambda: self.makePrivate(True))
        self.ui.privateNo.clicked.connect(lambda: self.makePrivate(False))
        

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


    def makePrivate(self, option):
            self.player.makePrivate(option)


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
        else:
            logging.debug("Cancel player deletion")


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.handleBack()


    def handleBack(self):
        self.switchModule(modules.MenuModule)
