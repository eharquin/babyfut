#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs : Yoann Malot, Thibaud Le Graverend
"""

import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from .. import modules
from ..core.module import Module
from common.settings import Settings
from ..ui.menu_ui import Ui_Form as MenuWidget
from common.side import Side
from common.module_switch import MenuSwitch

class MenuModule(Module):
    def __init__(self, parent):
        super().__init__(parent, MenuWidget())
        menuSwitch = MenuSwitch(self)
        # Button connections
        self.ui.btnStartQuick.clicked.connect(lambda: menuSwitch.authQuickModule())
        self.ui.btnStartLeague.clicked.connect(lambda: menuSwitch.tournamentModule())
        self.ui.btnLeaderboard.clicked.connect(lambda: menuSwitch.leaderboardModule())
        self.ui.btnOptions.clicked.connect(lambda: menuSwitch.optionsModule())
        self.ui.btnPrivacy.clicked.connect(lambda: menuSwitch.privacyModule())
        self.ui.btnEdit.clicked.connect(lambda: menuSwitch.editModule())

    def load(self):
        logging.debug('Loading MenuModule')
        self.ui.btnStartQuick.setFocus()

    def unload(self):
        logging.debug('Unloading MenuModule')

    def other(self, **kwargs):
        logging.debug('Other MenuModule')

        if 'rfid' in kwargs and 'source' in kwargs:
            self.send(modules.AuthQuickModule, **kwargs)
            self.ui.btnStartQuick.animateClick()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and Settings['app.mode']=='dev':
            self.handleExit()

        elif e.key() == Qt.Key_Up:
            self.parent().focusPreviousChild()

        elif e.key() == Qt.Key_Down:
            self.parent().focusNextChild()

        elif e.key() == Qt.Key_Left:
            self.send(modules.MenuModule, rfid=-2, source=Side.Left)

        elif e.key() == Qt.Key_Right:
            self.send(modules.MenuModule, rfid=-3, source=Side.Right)

        elif e.key() == Qt.Key_Return:
            if QApplication.focusWidget()==None:
                logging.error('No focused widget to activate')
            else:
                QApplication.focusWidget().animateClick()

    def handleExit(self):
        logging.info('Closing..')
        self.mainwin.close()
