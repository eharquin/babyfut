#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs : Yoann Malot, Thibaud Le Graverend
@modifs : Yaathavan Kumarasamy
"""

import os
from os.path import join, dirname, abspath
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsBlurEffect, QApplication, QMessageBox, QLabel
from PyQt5.QtCore import Qt, QTime, QTranslator, pyqtSlot, QThread

from .. import modules
from common.side import Side
from common.settings import Settings
from .main_ui import Ui_MainWindow
from ..core.server import Server

class MainWin(QtWidgets.QMainWindow):
    DEFAULT_LANG = 'en'
    TR_PATH = join(dirname(dirname(abspath(__file__))), 'translations/')

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lang = MainWin.DEFAULT_LANG
        self._retranslateUI()
        self.setWindowTitle('Babyfut')
        self.networkMessage = QMessageBox(self)


        #Background blur
        bgBlur = QGraphicsBlurEffect()
        bgBlur.setBlurHints(QGraphicsBlurEffect.QualityHint)
        #bgBlur.setBlurRadius(5)
        #self.ui.panels.setGraphicsEffect(bgBlur)

        # Module loading
        self.modules = [
            modules.WaitingModule(self),
            modules.MenuModule(self),
            modules.AuthQuickModule(self),
            modules.TournamentModule(self),
            modules.GameModule(self),
            modules.EndGameModule(self),
            modules.LeaderboardModule(self),
            modules.OptionsModule(self),
            modules.PrivacyModule(self),
            modules.EditModule(self),
            modules.TournamentParticipantModule(self),
            modules.TournamentDisplayModule(self)
        ]

        #Adding modules (Widgets) to the QStackedWidget panels
        for mod in self.modules:
            self.ui.panels.addWidget(mod)

        self.ui.panels.setCurrentIndex(0) #Showing the WaitingModule
        self.ui.panels.currentWidget().setFocus()
        self.ui.panels.setFocusProxy(self.ui.panels.currentWidget())
        self.ui.panels.currentWidget().load()
        self.displaySystemTime()
        self.startTimer(1000)

        self._loadSettings()

    #def eventFilter(target, event):
    #	return event.type()==QEvent.KeyPress and event.key() not in acceptedKeys

    def SwitchToMenuModule(self):
        self.ui.panels.setCurrentIndex(1) #Showing the MenuModule
        self.ui.panels.currentWidget().setFocus()
        self.ui.panels.setFocusProxy(self.ui.panels.currentWidget())
        self.ui.panels.currentWidget().load()
        self.displaySystemTime()
        self.startTimer(1000)
        self._loadSettings()

    def timerEvent(self, e):
        self.displaySystemTime()

    def displaySystemTime(self):
        self.ui.lcdTime.display(QTime.currentTime().toString("hh:mm:ss"))

    def findMod(self, type):
        mod_idx = [i for i, x in enumerate(self.modules) if isinstance(x, type)]
        return -1 if len(mod_idx)==0 else mod_idx[0]

    def dispatchMessage(self, msg, toType=None, toAll=False):
        if toType!=None:
            modulesIdx = [self.findMod(toType)]
        else:
            modulesIdx = self.modules if toAll else [self.findMod(type(self.ui.panels.currentWidget()))]

        for modIdx in modulesIdx:
            self.modules[modIdx].other(**msg)
    
    def networkWarning(self, action, msg=None):
        if action=='display':
            self.networkMessage.setWindowTitle("Warning")
            self.networkMessage.setText(msg)
            self.networkMessage.addButton(QMessageBox.Ok)
            self.networkMessage.removeButton(self.networkMessage.button(QMessageBox.Ok))
            self.networkMessage.exec()
        elif action=='close':
            self.networkMessage.done(1)

    def _loadSettings(self):
        if Settings['ui.fullscreen']:
            self.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)
        else:
            self.showMaximized()
            QApplication.setOverrideCursor(Qt.ArrowCursor)

        self._retranslateUI()

    def _retranslateUI(self):
        app = QApplication.instance()
        oldlang = self.lang
        newlang = Settings['ui.language']

        if newlang==oldlang:
            pass # Nothing to do

        elif newlang!=MainWin.DEFAULT_LANG:
            self.translator = QTranslator()
            if self.translator.load("babyfut_{}".format(newlang), MainWin.TR_PATH):
                logging.info('Installing \'{}\''.format(newlang))
                app.installTranslator(self.translator)
            else:
                logging.warn('Could not open translation file for \'{}\' in path "{}"'.format(newlang, MainWin.TR_PATH))

        elif newlang==MainWin.DEFAULT_LANG:
            logging.info('Installing language \'{}\''.format(newlang))
            app.removeTranslator(self.translator)
            self.translator = None

        self.lang = newlang
    
    def connect_slaves(self):
        self.thread = QThread()
        self.server = Server()
        self.server.moveToThread(self.thread)

        self.thread.started.connect(self.server.connect_slaves)
        self.server.slaves_connected.connect(self.message_signals)
        self.server.slaves_connected.connect(self.SwitchToMenuModule) # after connection : waiting -> menu Module
        self.thread.start()

    def message_signals(self):
        self.server.goalSignal.connect(lambda side	: self.dispatchMessage({'goal': True, 'source': side}))
        self.server.rfidSignal.connect(lambda side, rfid	: self.dispatchMessage({'rfid': rfid, 'source': side}))
        self.server.clientLostSignal.connect(lambda action, msg	: self.networkWarning(action, msg))
    
    def stop(self):
        self.server.stop()
        self.server.finished.connect(self.thread.quit) # quit the thread
        self.thread.finished.connect(self.thread.deleteLater)