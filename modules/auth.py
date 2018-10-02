#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import QTime, Qt

from module import Module
import modules
from ui.auth2p_ui import Ui_Form as Auth2pWidget

class AuthModule(Module):
	def __init__(self, parent):
		super().__init__(parent, Auth2pWidget())

	def load(self):
		logging.debug('Loading AuthModule')

	def unload(self):
		logging.debug('Unloading AuthModule')

	def other(self, **kwargs):
		logging.debug('Other AuthModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.ui_handleClick_btnCancel()
		elif e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
			self.ui_handleClick_btnDone()

	def ui_handleClick_btnCancel(self):
		self.switchModule(modules.MenuModule)

	def ui_handleClick_btnDone(self):
		self.switchModule(modules.GameModule)
