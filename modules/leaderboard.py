#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import QTime

from module import Module
import modules
from ui.leaderboard_ui import Ui_Form as LeaderboardWidget

class LeaderboardModule(Module):
	def __init__(self, parent):
		super().__init__(parent, LeaderboardWidget())
		
		self.ui.btnExit.clicked.connect(self.ui_handleClick_btnExit)

	def load(self):
		logging.debug('Loading LeaderboardModule')

	def unload(self):
		logging.debug('Unloading LeaderboardModule')

	def other(self, **kwargs):
		logging.debug('Other LeaderboardModule')

	def ui_handleClick_btnExit(self):
		self.switchModule(modules.MenuModule)
