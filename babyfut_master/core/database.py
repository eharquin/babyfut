#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import sqlite3
import logging
from os.path import exists
from ..babyfut_master import getContent
from .database_creator import createDatabase

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
		
	def _exec(self, query, args=()):
		try:
			return self._cursor.execute(query, args)
		except sqlite3.Error as err:
			logging.error('sqlite3 error : {}'.format(err))
			raise DatabaseError() from err

	def loginExists(self, login):
		return bool(self._exec('SELECT login FROM Players WHERE login==?', (login,)).fetchone())

	def selectPlayer(self, login):
		query = 'SELECT login, fname, lname, elo, private FROM Players WHERE login==?'
		return self._exec(query, (login,)).fetchone()

	def selectTeam(self, id):
		query = '''SELECT id, name, player1, player2 FROM Teams WHERE id==?'''
		return self._exec(query, (id,)).fetchone()

	def selectStats(self, login):
		query="SELECT SUM(M.duration) AS timePlayed, \
		SUM(CASE WHEN Teams.id=M.team1 THEN M.score1 ELSE M.score2 END ) AS goalsScored, \
		COUNT(*) AS gamesPlayed, \
		COUNT (CASE WHEN Teams.id=M.winningteam THEN '1' ELSE NULL END) AS victories\
		FROM Teams INNER JOIN  viewMatchs M ON (Teams.id==M.team1 OR Teams.id==M.team2) \
		WHERE (Teams.player1==? OR player2==?)"
		return self._exec(query, (login, login)).fetchone()


	# def _selectOne(self, query, *args):
	# 	#Base query function
	# 	return self._cursor.execute(query, args).fetchone()

	def insertPlayer(self, login, fname, lname, elo, private=0):
		self._exec('INSERT INTO Players (login, fname, lname, elo, private) VALUES (?, ?, ?, ?, ?)', (login, fname, lname, elo, private))
		self._connection.commit()
		return self._exec('SELECT login FROM Players WHERE login=?',(login,)).fetchone()[0]

	def checkTeam(self, *logins):
		if len(logins)==1:
			args = (logins[0],)
			query = "SELECT * FROM Teams WHERE player1=? AND player2 IS NULL AND NAME IS NULL"
		elif len(logins)==2:
			query="SELECT * FROM Teams WHERE (player1=? AND player2=? OR player1=? AND player2=?) AND NAME IS NOT NULL"
			args = (logins[0], logins[1], logins[1], logins[0])
		else:
			raise DatabaseError('Argument must be a list of 1 or 2 logins')	
		return self._exec(query, args).fetchone()

	def insertTeam(self, login1, login2=None, name=None):
		if not login2 and not name:
			self._exec('INSERT INTO Teams (player1) VALUES (?)', (login1,))
		elif login2 and name and name != 'NULL':
			args = (name, login1, login2)
			self._exec('INSERT INTO Teams (name, player1, player2) VALUES (?, ?, ?)', args)
		else:
			raise DatabaseError('Not a valid Team format')
		
		
		self._connection.commit()
		#Returns the new Team auto-incremented ID 
		return self._exec('SELECT seq FROM sqlite_sequence WHERE name="Teams"').fetchone()[0]

	def insertMatch(self, start_time, duration, team1, score1, team2, score2):
		args = (start_time, 1,  duration, team1, score1, team2, score2)
		self._exec('INSERT INTO Matchs (timestamp, babyfoot, duration, team1 ,score1, team2, score2) VALUES (?, ?, ?, ?, ?, ?, ?)', args)
		self._connection.commit()

	def selectAllPlayer(self):
		return self._exec('SELECT login, fname, lname FROM Players WHERE private==0').fetchall()

	def deletePlayer(self, login):
		self._exec('UPDATE Teams SET player1=NULL WHERE player1==?',(login,))
		self._exec('UPDATE Teams SET player2=NULL WHERE player2==?',(login,))
		self._exec('DELETE FROM Players WHERE login==?', (login,))
		self._connection.commit()

	def setPlayerPrivate(self, login, option):
		if option == True:
			self._exec("UPDATE Players SET private=1 WHERE login==?", (login,))
		elif option == False:
			self._exec("UPDATE Players SET private=0 WHERE login==?", (login,))
		self._connection.commit()

	# Return all the teams with the given player
	def selectPlayerTeams(self, login):
		return self._exec('SELECT id, name, player1, player2 FROM Teams WHERE (player1==? OR player2==?) AND name IS NOT NULL', (login, login,)).fetchall()

	# Return games played by the given player 
	def selectPlayerGames(self, login):
		query = '''SELECT timestamp, team1, score1, team2, score2, winningTeam FROM viewMatchs JOIN teams 
		ON viewMatchs.team1==teams.id OR viewMatchs.team2==teams.id WHERE player1==? OR player2==?
		ORDER BY timestamp DESC'''
		return self._exec(query,(login, login)).fetchall()

	def setEloRating(self, login, elo):
		self._exec("UPDATE Players SET elo=? WHERE login==?", (elo, login))
		self._connection.commit()

	def setTeamName(self, id, name):
		query = '''UPDATE Teams SET name = ? WHERE id=?'''
		self._exec(query, (name, id))
		self._connection.commit()


	def close(self):
		self._connection.close()

	@staticmethod
	def createDatabase(db_path):
		createDatabase(db_path)

	#Create a tournament open for register
	def createTn():
		pass
	
	#Returns all tournaments from a status, all of them if None
	def selectAllTn(status=None):
		pass
	
	#Closes registration, creates all games and set status running
	def validateTn():
		pass

	#Register a team to a future tournament
	def registerTeamTn():
		pass

	#Returns all Teams registered to a tournament
	def selectTeamsTn():
		pass
	
	#Returns all Matchs of a tournament
	def selectMatchsTn():
		pass
	
	#Insert scores of a tournament Match which has just been played
	def insertMatchTn():
		pass

	#Update the teams of the Tree Matchs when they are known
	def updateTreeMatchsTn():
		pass






#------INSERT TESTING DATA

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