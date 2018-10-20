#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
from enum import Enum

class Side(Enum):
	'''
	Values of the enum are used throughout the code for indexing purposes, not to be changed
	'''
	Undef = -1
	Left  = 0
	Right = 1

class Player():
	def __init__(self, id, fname='', lname='', pic_path=':ui/img/placeholder_head.jpg'):
		self.id = id
		self.fname = fname
		self.lname = lname
		self.pic_path = pic_path
		self.stats = Stat(id)
		
	@staticmethod
	def fromRFID(id):
		fname, lname, pic_url = '','','' # Replace with DB calls
			
		if id==-1:
			player = Player(id, 'Guest')
			
		elif id==-2:
			player = Player(id, 'Alfredo', 'Enrique')
			
		elif id==-3:
			player = Player(id, 'Bastien', 'Dali')
			player.stats.victories = 1
			
		elif id==-4:
			player = Player(id, 'Carim', 'Cuebache')
			player.stats.time_played = 1
			
		elif id==-5:
			player = Player(id, 'Dorian', 'Boulet')
			player.stats.games_played = 1
			
		elif id==-6:
			player = Player(id, 'Enzo', 'Arobaz')
			player.stats.goals_scored = 1
			
		else:
			player = Player(id, fname, lname, pic_url)
		
		return player
	
	def displayImg(self, containerWidget):
		containerWidget.setStyleSheet('border-image: url({});'.format(self.pic_path))
	
	def save(self):
		'''
		Update or create the player in database
		'''
		# TODO
		pass
	
	@property
	def name(self):
		return '{} {}'.format(self.fname, self.lname.upper())
	
	@property
	def pic(self):
		return QPixmap(self.pic_path)

class Stat():
	def __init__(self, player_id):
		self.victories    = 0
		self.time_played  = 0
		self.games_played = 0
		self.goals_scored = 0
		
		if player_id >= 0:
			self.victories    = 0
			self.time_played  = 0
			self.games_played = 0
			self.goals_scored = 0

PlayerGuest = Player.fromRFID(-1)
