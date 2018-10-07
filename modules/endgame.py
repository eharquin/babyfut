#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegion
from PyQt5.QtCore import QTime, QTimer, QRect, Qt

from module import Module
import modules
from ui.endgame_ui import Ui_Form as GameWidget

class EndGameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, GameWidget())
		self.screenTimeout = QTimer()
		self.screenTimeout.timeout.connect(self.ui_handleClick_btnQuit)
		self.screenTimeout.setSingleShot(True)

	def load(self):
		logging.debug('Loading EndGameModule')
		
		self.ui.lblP2_2.setText('Player {}'.format(self.winner+1))
		
		# Quit the screen after 5 seconds if the user doesn't do it before
		self.screenTimeout.start(5000)

	def unload(self):
		logging.debug('Unloading EndGameModule')
		self.screenTimeout.stop()
		self.winner = -1
	
	def other(self, **kwargs):
		logging.debug('Other EndGameModule')
		
		if 'winner' in kwargs:
			self.winner = kwargs['winner']
		
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Return:
			self.ui_handleClick_btnQuit()
	
	def ui_handleClick_btnQuit(self):
		self.switchModule(modules.MenuModule)
