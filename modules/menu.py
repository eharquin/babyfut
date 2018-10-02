#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from module import Module
import modules
from ui.menu_ui import Ui_Form as MenuWidget

class MenuModule(Module):
	def __init__(self, parent):
		super().__init__(parent, MenuWidget())

		# Button connections
		self.ui.btnStart2p.clicked.connect    (lambda: self.switchModule(modules.AuthModule))
		self.ui.btnStartParty.clicked.connect (lambda: self.switchModule(modules.GameModule))
		self.ui.btnStartLeague.clicked.connect(lambda: self.switchModule(modules.GameModule))
		self.ui.btnLeaderboard.clicked.connect(lambda: self.switchModule(modules.LeaderboardModule))
		self.ui.btnOptions.clicked.connect    (lambda: self.switchModule(modules.OptionsModule))

	def load(self):
		logging.debug('Loading MenuModule')
		self.ui.btnStart2p.setFocus()

	def unload(self):
		logging.debug('Unloading MenuModule')
	
	def other(self, **kwargs):
		logging.debug('Other MenuModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.ui_handleClick_btnExit()
		elif e.key() == Qt.Key_Up:
			self.parent().focusPreviousChild()
		elif e.key() == Qt.Key_Down:
			self.parent().focusNextChild()
		elif e.key() == Qt.Key_Return:
			QApplication.focusWidget().animateClick()

	def ui_handleClick_btnExit(self):
		logging.info('Closing..')
		self.parent_win.close()
