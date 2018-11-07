#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtWidgets import QAbstractItemView
from module import Module
from modules.auth import AuthModuleBase
from ui.authleague_ui import Ui_Form as AuthLeagueWidget

from player import Side, PlayerEmpty

class AuthLeagueModule(AuthModuleBase):
	def __init__(self, parent):
		super().__init__(parent, AuthLeagueWidget())
		
	def load(self):
		logging.debug('Loading AuthLeagueModule')
		super().load()
		self.addPlayer(Side.Left, PlayerEmpty)
		
	def unload(self):
		logging.debug('Loading AuthLeagueModule')
		super().unload()
		self.ui.playersList.clear()
	
	def createPlayerList(self):
		'''
		Duplicates the player list to be the same on both sides.
		That way, adding a player on the left or on the right have the exact same effect,
		and thus the AuthModuleBase code can remain generic.
		'''
		
		l = list()
		self.players = {Side.Left: l, Side.Right: l}
	
	def addPlayer(self, side, player):
		# Add the player if not already in the list
		if all([p.id!=player.id for p in self.players[side]]):
			if player!=PlayerEmpty:
				self.players[side].append(player)
			
			# Update the left side description
			player.displayImg(self.ui.img)
			self.ui.lblName.setText(player.name)
			self.ui.lblStat1.setText('{} Victories'.format(player.stats['victories']))
			self.ui.lblStat2.setText('{} Games Played'.format(player.stats['games_played']))
			self.ui.lblStat3.setText('{} Goals Scored'.format(player.stats['goals_scored']))
			
			if player!=PlayerEmpty:
				# Update the right side list, making sure that the added player is showed
				self.ui.playersList.addItem('{}. {}'.format(len(self.players[side]), player.name))
				widgetItem = self.ui.playersList.item(self.ui.playersList.count()-1)
				self.ui.playersList.scrollToItem(widgetItem, QAbstractItemView.PositionAtBottom)
	
	def handleDone(self):
		super().handleDone()