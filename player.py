#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
from enum import Enum

class Side(Enum):
	Undef = 0
	Left  = 1
	Right = 2

class Player():
	def __init__(self, id):
		fname, lname, pic_url = '','','' # Replace with DB calls
		self.__init__(id, fname, lname, pic_url)

	def __init__(self, id, fname, lname, pic_path):
		self.id = id
		self.fname = fname
		self.lname = lname
		self.pic_path = pic_path
		self.stats = Stat(id)
	
	def save(self):
		'''
		Update or create the player in database
		'''
		# TODO
		pass
	
	@property
	def name(self):
		return self.lname.upper() + self.fname
	
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

PlayerGuest = Player(-1, 'Guest', '', ':ui/img/placeholder_head.jpg')
