#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import Qt

from .. import modules #tout le package modules
from ..core.module import Module
from ..core.player import Side, Player

class AuthModuleBase(Module):
	def __init__(self, parent, widget):
		super().__init__(parent, widget)
		self.createPlayerList()
		self.numPlayers = 0

	def load(self):
		pass

	def unload(self):
		self.createPlayerList()
		self.numPlayers = 0

	def other(self, **kwargs):
		for key, val in kwargs.items():
			if key=='rfid' and 'source' in kwargs:
				side = kwargs['source']
				self.numPlayers += 1
				self.addPlayer(side, Player.fromRFID(val))

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleCancel()

		elif e.key() == Qt.Key_Return:
			self.handleDone()

		elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
			side = Side.Left if e.key() == Qt.Key_Left else Side.Right
			rfid = -(2 + self.numPlayers%5)
			self.send(type(self), rfid=rfid, source=side)

	def createPlayerList(self):
		logging.warning('Base function meant to be reimplemented')

	def handleCancel(self):
		self.switchModule(modules.MenuModule)

	def handleDone(self):
		self.send(modules.GameModule, players=self.players)
		self.switchModule(modules.GameModule)
