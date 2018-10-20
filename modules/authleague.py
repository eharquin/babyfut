#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from module import Module
from ui.authquick_ui import Ui_Form as AuthQuickWidget

class AuthLeagueModule(Module):
	def __init__(self, parent):
		super().__init__(parent, AuthQuickWidget())
		
	def load(self):
		logging.debug('Loading AuthLeagueModule')
		super().load()
		
	def unload(self):
		logging.debug('Loading AuthLeagueModule')
		super().load()
