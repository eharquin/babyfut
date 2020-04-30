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

	def loginExists(self, login):
		return bool(self._cursor.execute('SELECT login FROM Players WHERE login==?', [login]).fetchone())

	def selectPlayer(self, login):
		query = 'SELECT login, fname, lname, elo FROM Players WHERE login==?'
		return self._selectOne(query, login)

	def selectStats(self, login):
		query="SELECT SUM(Matchs.duration) AS timePlayed, \
		SUM(CASE WHEN Teams.id=Matchs.winningteam THEN Matchs.scoreWinner ELSE Matchs.scoreLoser END ) AS goalsScored, \
		COUNT(*) AS gamesPlayed, \
		COUNT (CASE WHEN Teams.id=Matchs.winningteam THEN '1' ELSE NULL END) AS victories\
		FROM Teams INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam OR Teams.id==Matchs.losingTeam) \
		WHERE (Teams.player1==? OR player2==?)"
		return self._selectOne(query, login, login)


	def _selectOne(self, query, *args):
		#Base query function
		res = self._cursor.execute(query, args).fetchone()
		if not res:
			raise DatabaseError('Query \"{}\" returned nothing with args {}'.format(query, args))
		return res

	# def select_guest_team(self):
	# 	return self.select_one('SELECT id FROM Players WHERE fname LIKE "guest"')[0]

	def insertPlayer(self, login, fname, lname, elo, private=0):
		self._cursor.execute('INSERT INTO Players (login, fname, lname, elo, private) VALUES (?, ?, ?, ?, ?)', (login, fname, lname, elo, private))
		self._connection.commit()
		return self._selectOne('SELECT login FROM Players WHERE login=?',(login))

	# Return select result
	def checkTeam(self, login1, login2='NULL'):
		args = (login1, login2, login2, login1)
		return self._selectOne('SELECT * FROM Teams WHERE player1=? AND player2=? OR player1=? AND player2=?', *args )

	def insertTeam(self, name, login1, login2='NULL'):
		self._cursor.execute('INSERT INTO Teams (name, player1, player2) VALUES (?, ?, ?)', (name, login1, login2))
		self._connection.commit()
		return self._cursor.execute('SELECT seq FROM sqlite_sequence WHERE name="Teams"').fetchone()[0]

	def insertMatch(self, start_time, duration, WTeam, scoreW, LTeam, scoreL):
		args = (start_time, 1,  duration, WTeam, scoreW,LTeam, scoreL)
		self._cursor.execute('INSERT INTO Matchs (timestamp, babyfoot, duration, winningTeam,scoreWinner, losingTeam, scoreLoser) VALUES (?, ?, ?, ?, ?, ?, ?)', args)
		self._connection.commit()

	def selectAllPlayer(self):
		return self._cursor.execute('SELECT login, fname, lname FROM Players WHERE private==0').fetchall()

	# def deletePlayer(self, playerID):
	# 	self._cursor.execute('DELETE FROM Players WHERE id==?', (playerID,))
	# 	self._connection.commit()

	# def deletePicture(self, playerID):
	# 	self._cursor.execute('UPDATE Players SET login=null WHERE id==?', (playerID,))
	# 	self._connection.commit()

	def setPlayerPrivate(self, login):
		self._cursor.execute("UPDATE Players SET private=1 WHERE login==?", [login])
		self._connection.commit()

	def setEloRating(self, login, elo):
		self._cursor.execute("UPDATE Players SET elo=? WHERE login==?", [elo, login])
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
				`winningTeam`	INTEGER REFERENCES Teams(id),
				`scoreWinner` INTEGER NOT NULL,
				`losingTeam`	INTEGER REFERENCES Teams(id),
				`scoreLoser` INTEGER NOT NULL,
				CHECK (scoreWinner > scoreLoser)
			)''')

			c.execute('''CREATE TABLE "Players" (
				`login` TEXT PRIMARY KEY,
				`fname`	TEXT NOT NULL,
				`lname`	TEXT NOT NULL,
				`elo` INTEGER,
				`private`	INTEGER NOT NULL CHECK(private == 0 or private == 1)
			)''')

			c.execute('''CREATE TABLE "Teams" (
				`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
				`name` TEXT,
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

# def ajoutMatch(start_time, duration, WTeam, scoreW, LTeam, scoreL):
# 	t1 = db.insertTeam(WTeam)
# 	t2 = db.insertTeam(LTeam)
# 	db.insertMatch(start_time, duration, t1, scoreW, t2, scoreL)

# db = Database.instance()
# db.insertPlayer('malotyoa', 'Yoann', 'Malot', 1500)
# db.insertPlayer('tlegrave', 'Thibaud', 'Le Graverend', 1500)
# db.insertPlayer('bonnetst', 'Stéphane', 'Bonnet', 1500)
# db.insertPlayer('sophsti', 'Sophie', 'Stické', 1500)
# db.insertPlayer('toalthe', 'Théo', 'Toalet', 1500)
# ajoutMatch(123, 12, ['malotyoa'], 5, ['tlegrave', 'bonnetst'], 2)
# ajoutMatch(124, 12, ['sophsti'], 10, ['toalthe'], 9)
# ajoutMatch(125, 78, ['toalthe'], 10, ['sophsti'], 3)
# db.insertPlayer('jambon', 'James', 'Bond', 1500)
# db.setPlayerPrivate('jambon')

#print([row for row in db.selectAllPlayer()])
#print(db.selectStats('malotyoa'))