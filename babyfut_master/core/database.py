#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann MALOT, Thibaud LE GRAVEREND
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
	
	def close(self):
		self._connection.close()

	@staticmethod
	def createDatabase(db_path):
		createDatabase(db_path)

#-----------------------PLAYERS--------------------------------

	def loginExists(self, login):
		return bool(self._exec('SELECT login FROM Players WHERE login==?', (login,)).fetchone())

	def selectPlayer(self, login):
		query = 'SELECT login, fname, lname, elo, private FROM Players WHERE login==?'
		return self._exec(query, (login,)).fetchone()

	def insertPlayer(self, login, fname, lname, elo, private=0):
		self._exec('INSERT INTO Players (login, fname, lname, elo, private) VALUES (?, ?, ?, ?, ?)', (login, fname, lname, elo, private))
		self._connection.commit()
		return self._exec('SELECT login FROM Players WHERE login=?',(login,)).fetchone()[0]

	def selectStats(self, login):
		query="SELECT SUM(M.duration) AS timePlayed, \
		SUM(CASE WHEN Teams.id=M.team1 THEN M.score1 ELSE M.score2 END ) AS goalsScored, \
		COUNT(*) AS gamesPlayed, \
		COUNT (CASE WHEN Teams.id=M.winningteam THEN '1' ELSE NULL END) AS victories\
		FROM Teams INNER JOIN  viewMatchs M ON (Teams.id==M.team1 OR Teams.id==M.team2) \
		WHERE (Teams.player1==? OR player2==?)"
		return self._exec(query, (login, login)).fetchone()

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


#----------------------TEAMS-------------------------------------


	def selectTeam(self, id):
		query = '''SELECT id, name, player1, player2 FROM Teams WHERE id==?'''
		return self._exec(query, (id,)).fetchone()

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

	def setTeamName(self, id, name):
		query = '''UPDATE Teams SET name = ? WHERE id=?'''
		self._exec(query, (name, id))
		self._connection.commit()

#------------------------------Matchs------------------------------------------

	def insertMatch(self, start_time, duration, team1, score1, team2, score2):
		args = (start_time, 1,  duration, team1, score1, team2, score2)
		self._exec('INSERT INTO Matchs (timestamp, babyfoot, duration, team1 ,score1, team2, score2) VALUES (?, ?, ?, ?, ?, ?, ?)', args)
		self._connection.commit()

#---------------------------Tournaments----------------------------------------------

	#Create a tournament open for register and returns its id
	def createTn(self, name, t):	
		query = "INSERT INTO Tournaments (name, status, type) VALUES (?,0,?)"
		self._exec(query, (name,t))
		self._connection.commit()
		return self._exec('SELECT seq FROM sqlite_sequence WHERE name="Tournaments"').fetchone()[0]
	
	def selectTn(self, id):
		return self._exec("SELECT id, name, status, type FROM Tournaments WHERE id==?",(id,)).fetchone()

	#Returns all tournaments from a status, all of them if None
	def selectAllTn(self, status=None):
		if status:
			result=self._exec('SELECT id, name, status, type FROM Tournaments \
			WHERE status==?',(Database.statusTn[status],)).fetchall()
		else:
			result=self._exec('SELECT id, name, status, type FROM Tournaments').fetchall()
		return result
	
	#Changes the tournament status
	def setStatusTn(self, id, status):
		if status in Database.statusTn:
			self._exec("UPDATE Tournaments SET status=? WHERE id==?", (Database.statusTn.index(status), id))
			self._connection.commit()


	#Register a team to a future tournament
	def registerTeamTn(self, team, tournament):
		checkStatus=self.selectTn(tournament)
		if (not checkStatus or checkStatus[3]!= 0):
	 		raise DatabaseError("Tournaments not existing or not in status Future")
		self._exec("INSERT INTO Participate (team,  tournament) VALUES (?,?)", (team, tournament))
		self._connection.commit()

	#Returns all Teams registered to a tournament
	def selectTeamsTn(self, id):
		query= '''SELECT T.id, name, player1, player2 FROM Teams T INNER JOIN Participate
		ON  T.id==Participate.team WHERE tournament==?'''
		return self._exec(query, (id,)).fetchall()
	
	#Returns all Matchs of a tournament
	def selectMatchsTn(self, id):
		query='''SELECT M.*, T.round, Tr.KOType, Tr.parent1, Tr.parent2
		FROM Matchs M INNER JOIN TournamentMatchs T ON T.id==M.id
		LEFT JOIN TreeMatchs Tr ON T.id==Tr.id
		WHERE T.tournament==?'''
		return self._exec(query, (id,)).fetchall()
	
	#Insert Match in a tournament. KOtype is 'W' or 'L'
	def createMatchTn(id, round, t1, t2, p1, p2, KOtype=None):
		if bool(t1)!=bool(p1) and bool(p2)!=bool(t2):
			match = self.insertMatch(None, None, None, t1, None, t2, None)
			self._exec("INSERT INTO TournamentMatch VALUES (?, ?, ?, ?, ?, ?)", (match, id, round, KOType,  p1, p2))


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