#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import Qt

from .. import modules #tout le package modules
from ..core.module import Module
from ..core.player import Player
from common.side import Side
from ..core.team import Team

class AuthModuleBase(Module):
	def __init__(self, parent, widget):
		super().__init__(parent, widget)
		self.createTeamList()
		self.numPlayers = 0

	def load(self):
		pass

	def unload(self):
		self.createTeamList()
		self.numPlayers = 0

	def other(self, **kwargs):
		for key, val in kwargs.items():
			if key=='rfid' and 'source' in kwargs:
				side = kwargs['source']
				self.numPlayers += 1
				newPlayer = Player.fromRFID(val)
				if not any(team.isPlayer(newPlayer) for team  in self.teams.values()):
					self.addPlayer(side, newPlayer)

	def keyPressEvent(self, e):
		#Simulating RFIDs in DB with keyboard
		dictKeysLeft = {Qt.Key_A :'123456AB', Qt.Key_Z :'ABCDABCD', Qt.Key_E :'YM', Qt.Key_R :'TLG',Qt.Key_T :'01234567'}
		dictKeysRight = {Qt.Key_Q :'123456AB', Qt.Key_S :'ABCDABCD', Qt.Key_D :'YM', Qt.Key_F:'TLG',Qt.Key_G :'01234567'}

		if e.key() == Qt.Key_Escape:
			self.handleCancel()

		elif e.key() == Qt.Key_Return:
			self.handleDone()

		# elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
		# 	side = Side.Left if e.key() == Qt.Key_Left else Side.Right
		# 	rfid = -(2 + self.numPlayers%5)
		# 	self.send(type(self), rfid=rfid, source=side)

		elif e.key() in dictKeysLeft.keys():
			self.other(rfid=dictKeysLeft[e.key()],  source =Side.Left)
		elif e.key() in dictKeysRight.keys():
			self.other(rfid=dictKeysRight[e.key()],  source =Side.Right)

	def createPlayerList(self):
		logging.warning('Base function meant to be reimplemented')

	def handleCancel(self):
		self.switchModule(modules.MenuModule)

	def handleDone(self):
		self.send(modules.GameModule, teams=self.teams)
		self.switchModule(modules.GameModule)
