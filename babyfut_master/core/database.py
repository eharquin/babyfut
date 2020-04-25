#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sqlite3
from os.path import exists
from ..babyfut_master import getContent

class DatabaseError(Exception):
	pass

class Database():
	__db = None

	def __init__(self):
		if not Database.__db:
			db_path = getContent('babyfut.sqlite')
			if not exists(db_path):
				Database.createDatabase(db_path)

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

	def rfidExists(self, rfid):
		return bool(self._cursor.execute('SELECT rfid FROM Players WHERE rfid==?', (rfid,)).fetchone())

	def selectPlayer(self, rfid):
		query = 'SELECT id, login, fname, lname FROM Players WHERE rfid==?'
		return self._selectOne(query, rfid)

	def selectStats(self, rfid):
		query="SELECT SUM(Matchs.duration) AS timePlayed, \
		SUM(Teams.nGoals) AS goalsScored, \
		COUNT(*) AS gamesPlayed, \
		COUNT (CASE WHEN Teams.id=Matchs.winningteam THEN '1' ELSE NULL END) AS victories\
		FROM Teams INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam OR Teams.id==Matchs.losingTeam) \
		WHERE (Teams.player1==? OR player2==?)"
		return self._selectOne(query, rfid, rfid)


	def _selectOne(self, query, *args):
		#Base query function
		res = self._cursor.execute(query, args).fetchone()
		if not res:
			raise DatabaseError('Query \"{}\" returned nothing with args {}'.format(query, args))
		return res

	# def select_guest_team(self):
	# 	return self.select_one('SELECT id FROM Players WHERE fname LIKE "guest"')[0]

	def insertPlayer(self, login, rfid, fname, lname, private=0):
		self._cursor.execute('INSERT INTO Players (login, rfid, fname, lname, private) VALUES (?, ?, ?, ?, ?)', (login, rfid, fname, lname, private))
		self._connection.commit()
		return self._selectOne('SELECT login FROM Players WHERE login=?',(login))

	def insertTeam(self, logins):
		if len(players)<2:
			logins.append('NULL')
		#Checking if the Team is already in  DB
		args = (logins[1], logins[2], logins[2], logins[1])
		rep = self._cursor.execute('SELECT * FROM Teams WHERE player1=? AND player2=? OR player1=? AND player2=?', args )
		if len(rep)==0:
			self._cursor.execute('INSERT INTO Teams (player1, player2) VALUES (?, ?)', (player[0], players[1]))
			self._connection.commit()
			return self._cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="Teams"').fetchone()[0]
		else:
			return rep.fetchone()[0]

	def insertMatch(self, start_time, duration, WTeam, scoreW, LTeam, scoreL):
		args = (start_time, 1,  duration, WTeam, scoreW,LTeam, scoreL)
		self._cursor.execute('INSERT INTO Matchs (timestamp, babyfoot, duration, winningTeam,scoreWinner, losingTeam, scoreLoser) VALUES (?, ?, ?, ?, ?, ?, ?)', args)
		self._connection.commit()

	def select_all_rfid(self, debug=False):
		return self._cursor.execute('SELECT rfid FROM Players WHERE private==0').fetchall()

	# def deletePlayer(self, playerID):
	# 	self._cursor.execute('DELETE FROM Players WHERE id==?', (playerID,))
	# 	self._connection.commit()

	# def deletePicture(self, playerID):
	# 	self._cursor.execute('UPDATE Players SET login=null WHERE id==?', (playerID,))
	# 	self._connection.commit()

	def setPlayerPrivate(self, login):
		self._cursor.execute('UPDATE Players SET private=1 WHERE login==?', (login))
		self._connection.commit()

	def close(self):
		self._connection.close()

	@staticmethod
	def createDatabase(db_path):
			conn = sqlite3.connect(db_path)
			c = conn.cursor()

			c.execute('''CREATE TABLE "Matchs" (
				`id` INTEGER PRIMARY KEY AUTOINCREMENT,
				`timestamp`	INTEGER NOT NULL,
				`babyfoot` NOT NULL REFERENCES Babyfoots(id),
				`duration`	INTEGER NOT NULL,
				`winningTeam`	INTEGER NOT NULL REFERENCES Teams(id),
				`scoreWinner` INTEGER NOT NULL,
				`losingTeam`	INTEGER NOT NULL REFERENCES Teams(id),
				`scoreLoser` INTEGER NOT NULL
			)''')

			c.execute('''CREATE TABLE "Players" (
				`login` TEXT PRIMARY KEY,
				`rfid`	INTEGER NOT NULL UNIQUE,
				`fname`	TEXT NOT NULL,
				`lname`	TEXT NOT NULL,
				`private`	INTEGER NOT NULL CHECK(private == 0 or private == 1)
			)''')

			c.execute('''CREATE TABLE "Teams" (
				`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
				`player1`	TEXT NOT NULL REFERENCES Players(login),
				`player2`	TEXT REFERENCES Players(login)
			)''')

			c.execute('''CREATE TABLE "Babyfoots" (
				`id` INTEGER PRIMARY KEY AUTOINCREMENT,
				`location` TEXT
			)
			
			''')
			c.execute("INSERT INTO Babyfoots (location) VALUES ('Fablab')")
			
			conn.commit()
			c.close()


