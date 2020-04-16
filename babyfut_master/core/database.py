#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sqlite3

from ..babyfut_master import getContent

class DatabaseError(Exception):
	pass

class Database():
	__db = None

	def __init__(self):
		if not Database.__db:
			db_path = getContent('babyfut.sqlite')
			self._connection = sqlite3.connect(db_path)

	@staticmethod
	def instance():
		'''
		Singleton
		'''
		if not Database.__db:
			Database.__db = Database()

		return Database.__db

	@property
	def _cursor(self):
		return self._connection.cursor()

	def rfid_exists(self, rfid):
		return bool(self._cursor.execute('SELECT rfid FROM Players WHERE rfid==?', (rfid,)).fetchone())

	def select_one(self, query, *args):
		res = self._cursor.execute(query, args).fetchone()
		if not res:
			raise DatabaseError('Query \"{}\" returned nothing with args {}'.format(query, args))

		return res

	def select_guest_team(self):
		return self.select_one('SELECT id FROM Players WHERE fname LIKE "guest"')[0]

	def insert_player(self, rfid, fname, lname,):
		self._cursor.execute('INSERT INTO Players (rfid, fname, lname, category, pic, private) VALUES (?, ?, ?, ?, ?)', (rfid, fname, lname, None, 0,))
		self._connection.commit()
		return self._cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="Players"').fetchone()[0]

	def insert_team(self, players, goals):
		if len(players)<2:
			players.append(None)

		self._cursor.execute('INSERT INTO Teams (nGoals, player1, player2) VALUES (?, ?, ?)', (goals, players[0], players[1],))
		self._connection.commit()
		return self._cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="Teams"').fetchone()[0]

	def insert_match(self, start_time, duration, team1, team2):
		self._cursor.execute('INSERT INTO Matchs (timestamp, duration, winningTeam, losingTeam) VALUES (?, ?, ?, ?)', (start_time, duration, team1, team2,))
		self._connection.commit()

	def select_all_rfid(self, debug=False):
		from common.settings import Settings
		if Settings['app.mode']=='prod':
			return self._cursor.execute('SELECT rfid FROM Players WHERE rfid>0 AND private==0').fetchall()
		else:
			return self._cursor.execute('SELECT rfid FROM Players WHERE rfid<-1 AND private==0').fetchall()

	def delete_player(self, playerID):
		self._cursor.execute('DELETE FROM Players WHERE id==?', (playerID,))
		self._connection.commit()

	def delete_playerpic(self, playerID):
		self._cursor.execute('UPDATE Players SET login=null WHERE id==?', (playerID,))
		self._connection.commit()

	def make_player_private(self, playerID):
		self._cursor.execute('UPDATE Players SET private=1 WHERE id==?', (playerID,))
		self._connection.commit()

	def close(self):
		self._connection.close()