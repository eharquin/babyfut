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

import modules
from module import Module
from settings import Settings
from ui.menu_ui import Ui_Form as MenuWidget
from player import Side

class MenuModule(Module):
	def __init__(self, parent):
		super().__init__(parent, MenuWidget())

		# Button connections
		self.ui.btnStartQuick.clicked.connect (lambda: self.switchModule(modules.AuthQuickModule))
		self.ui.btnStartLeague.clicked.connect(lambda: self.switchModule(modules.AuthLeagueModule))
		self.ui.btnLeaderboard.clicked.connect(lambda: self.switchModule(modules.LeaderboardModule))
		self.ui.btnOptions.clicked.connect    (lambda: self.switchModule(modules.OptionsModule))

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
			self.send(modules.MenuModule, rfid=-4, source=Side.Right)
			
		elif e.key() == Qt.Key_Return:
			if QApplication.focusWidget()==None:
				logging.error('No focused widget to activate')
			else:
				QApplication.focusWidget().animateClick()
	
	def handleExit(self):
		logging.info('Closing..')
		self.mainwin.close()
