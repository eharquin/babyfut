#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
import sqlite3

from enum import Enum

class Side(Enum):
	'''
	Values of the enum are used throughout the code for indexing purposes, not to be changed
	'''
	Undef = -1
	Left  = 0
	Right = 1
	
	@property
	def opposite(self):
		return Side.Right if self==Side.Left else Side.Left 

from database import Database, DatabaseError

class Player():
	__query_infos = 'SELECT id, fname, lname, pic FROM Players WHERE rfid==?'
	__query_time_goals_games = 'SELECT SUM(Matchs.duration) AS timePlayed, SUM(Teams.nGoals) AS goalsScored, COUNT(*) AS gamesPlayed FROM Teams INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam OR Teams.id==Matchs.losingTeam) WHERE (Teams.player1==? OR player2==?)'
	__query_victories = 'SELECT COUNT(*) AS victories FROM Players INNER JOIN Teams ON (Players.id==Teams.player1 OR Players.id==Teams.player2) INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam) WHERE Players.id==?'

	_placeholder_pic_path = ':ui/img/placeholder_head.jpg'
	
	def __init__(self, id, rfid, fname, lname, pic_path, stats):
		self.id = id
		self.rfid = rfid
		self.fname = fname
		self.lname = lname
		self.pic_path = pic_path if pic_path else Player._placeholder_pic_path # Default pic if None
		self.stats = stats
	
	@staticmethod
	def fromRFID(rfid):
		db = Database.instance()
		
		try:
			# Retrieve generic informations
			id, fname, lname, pic = db.select_one(Player.__query_infos, rfid)
			
			# Retrieve stats
			stats = {}
			stats['time_played'], stats['goals_scored'], stats['games_played'] = db.select_one(Player.__query_time_goals_games, id, id)
			stats['victories'], = db.select_one(Player.__query_victories, id)
			
			for key, val in stats.items():
				if val==None:
					stats[key] = 0
			
			return Player(id, rfid, fname, lname, pic, stats)
		
		except DatabaseError as e:
			logging.warn('DB Error: {}'.format(e))
			return PlayerGuest
	
	def displayImg(self, containerWidget):
		containerWidget.setStyleSheet('border-image: url({});'.format(self.pic_path))
	
	def save(self):
		'''
		Update or create the player in database
		'''
	
	@property
	def name(self):
		return '{} {}'.format(self.fname, self.lname.upper())
		
	@property
	def stats_property(self):
		'''
		Compatibility property allowing to access stats as a object member and not dict
		ex: player.stats['victories'] can be accessed with player.stats_property.victories'
		This is mostly used for sorting players in leaderboard.py
		'''
		class Stat:
			def __init__(self, stats):
				self.victories = stats['victories']
				self.time_played = stats['time_played']
				self.goals_scored = stats['goals_scored']
				self.games_played = stats['games_played']
		
		return Stat(self.stats)
	
	@staticmethod
	def allPlayers():
		return [Player.fromRFID(rfid) for rfid, in Database.instance().select_all_rfid()]

PlayerGuest = Player.fromRFID(-1)
PlayerEmpty = Player(-1, -42, '', '', Player._placeholder_pic_path, {'time_played':'', 'goals_scored':'', 'games_played':'', 'victories': ''})
