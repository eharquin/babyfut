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
				if not any(team.hasPlayer(newPlayer) for team  in self.teams.values()):
					self.addPlayer(side, newPlayer)
			

	def keyPressEvent(self, e):
		#Simulating RFIDs in DB with keyboard
		dictKeysLeft = {Qt.Key_A :'123456AB', Qt.Key_Z :'ABCDABCD', Qt.Key_E :'01234567', Qt.Key_R :'TLG',Qt.Key_T :'SB',\
		Qt.Key_Y :'YM', Qt.Key_U :'TT', Qt.Key_I :'SS', Qt.Key_O:'JB'}
		dictKeysRight = {Qt.Key_Q :'123456AB', Qt.Key_S :'ABCDABCD', Qt.Key_D :'01234567', Qt.Key_F:'TLG',Qt.Key_G :'SB',\
		Qt.Key_H :'YM', Qt.Key_J :'TT', Qt.Key_K :'SS', Qt.Key_L:'JB'}
		
		if e.key() == Qt.Key_Escape:
			self.handleCancel()

		elif e.key() == Qt.Key_Return:
			self.handleDone()

		elif e.key() in dictKeysLeft.keys():
			self.other(rfid=dictKeysLeft[e.key()],  source =Side.Left)
		elif e.key() in dictKeysRight.keys():
			self.other(rfid=dictKeysRight[e.key()],  source =Side.Right)

	def createTeamList(self):
		logging.warning('Base function meant to be reimplemented')

	def handleCancel(self):
		self.switchModule(modules.MenuModule)

	def handleDone(self):
		for team in self.teams.values():
			team.insertDB()
		self.send(modules.GameModule, teams=self.teams)
		self.switchModule(modules.GameModule)
