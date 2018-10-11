#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import QTime, Qt

from module import Module
from player import Side
import modules
from ui.auth2p_ui import Ui_Form as Auth2pWidget

class AuthModule(Module):
	def __init__(self, parent):
		super().__init__(parent, Auth2pWidget())

	def load(self):
		logging.debug('Loading AuthModule')
		self.players = {Side.Left: list(), Side.Right: list()}

	def unload(self):
		logging.debug('Unloading AuthModule')
		del self.players

	def other(self, **kwargs):
		logging.debug('Other AuthModule')
		
		for key, val in kwargs.items():
			if key=='ardl_rfid' or key=='ardr_rfid':
				side = Side.Left if key.startswith('ardl') else Side.Right
				self.players.append(Player(val))

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleCancel()
		elif e.key() == Qt.Key_Return:
			self.handleDone()

	def handleCancel(self):
		self.switchModule(modules.MenuModule)

	def handleDone(self):
		self.send(modules.GameModule, players=self.players)
		self.switchModule(modules.GameModule)
