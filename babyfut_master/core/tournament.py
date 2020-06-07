#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann MALOT, Thibaud LE GRAVEREND
"""

from PyQt5.QtCore import QObject

from ..core.player import Player
from .database import Database, DatabaseError
from .team import Team
from enum import Enum
from random import choice
import math

class TournamentType(Enum):
	Elimination = 0
	Double = 1 
	EliminationQualif = 2
	DoubleQualif = 3
	Qualif = 4

class TournamentStatus(Enum):
	Future = 0
	Running = 1 
	Past = 2
	Cancelled = 3

class Tournament(QObject):

	def __init__(self, id, name, status, _type):
		QObject.__init__(self)
		self.id = id
		self.name = name
		self.status = status
		self.type = _type
		self.teams = list()
		self.matchs = list()
		teamdict= dict()
		matchdict = dict()


		for t in Database.instance().selectTeamsTn(self.id):
			players = [Player.loadFromDB(t[2])]
			if t[3]:
				players.append(Player.loadFromDB(t[3]))
			team = Team(t[0], t[1], players)
			teamdict[t[0]] = team
			self.teams.append(team)
		
		for m in Database.instance().selectMatchsTn(self.id):
			t1 =teamdict[m[4]] if m[4] else None
			t2 =teamdict[m[6]] if m[6] else None
			match = Tournament.Match(m[0], self, m[8], t1,t2, m[10],m[11], m[9])
			if m[5]!=None and m[7]!=None:
				match.scores=[m[5], m[7]]
				match.played=True
			self.matchs.append(match)

		
		for m in self.matchs:
			matchdict[m.id] = m

		for m in self.matchs:
			m.parents[0] = matchdict[m.parents[0]] if m.parents[0] else None
			m.parents[1] = matchdict[m.parents[1]] if m.parents[1] else None


		self.currentRound=max([m.round for m in self.matchs if not m.played]) if self.status==TournamentStatus.Running else None
		#self.updateTree()

	def registerTeam(self, team):
		if self.status == TournamentStatus.Future:
			self.teams.append(team)
			Database.instance().registerTeamTn(team.id, self.id)

	def updateTree(self):
		if self.status==TournamentStatus.Running:
			for match in self.matchs:
				for i in [0,1]:
					modified=False
					if match.teams[i]==None and match.parents[i] and match.parents[i].played:
						match.teams[i] = match.parents[i].teamResult(match.KOtype)
						modified=True
				if modified:
					t1=match.teams[0].id if match.teams[0] else None
					t2=match.teams[1].id if match.teams[1] else None
					Database.instance().updateTreeMatchTn(match.id, t1, t2)
			if all(m.played for m in self.matchs if m.playable()):
				self.currentRound -= 1	
				if self.currentRound==0:
					self.status=TournamentStatus.Past
					Database.instance().setStatusTn(self.id, self.status)

				



	@property
	def rounds(self):
		rounds = dict(list())
		for m in self.matchs:
			if m.roundName() in rounds.keys():
				rounds[m.roundName()].append(m)
			else:
				rounds[m.roundName()] = [m]
		return rounds

	
	@staticmethod
	def selectAll(status=None):
		if status:
			status = status.value
		return [Tournament(int(t[0]), t[1], TournamentStatus(int(t[2])), TournamentType(int(t[3]))) for t in Database.instance().selectAllTn(status)]

	@staticmethod
	def create(name, _type):
		id = Database.instance().createTn(name, _type.value)
		return Tournament(id, name, TournamentStatus.Future, _type)

	def validate(self):
		if self.status == TournamentStatus.Future:
			liste = self.teams
			nextliste=list()
			if self.type==TournamentType.Elimination:
				nbteams = len(liste)
				nbrounds = math.floor(math.log2(nbteams))
				nbsupmatchs = int(nbteams-math.pow(2,nbrounds))
				for i in range(nbsupmatchs):
					t1 = choice(liste)
					liste.remove(t1)
					t2 = choice(liste)
					liste.remove(t2)
					match = Tournament.Match.create(self, int(nbrounds+1), t1, t2, 'W')
					nextliste.append(match)
					self.matchs.append(match)
				nextliste += liste
				
				for round in range(nbrounds, 0, -1):
					liste=nextliste.copy()
					nextliste.clear()				
					for j in range(0, int(pow(2, round-1))):
						t1=choice(liste)
						liste.remove(t1)
						t2=choice(liste)
						liste.remove(t2)
						match=Tournament.Match.create(self,int(round), t1, t2, 'W' )
						self.matchs.append(match)
						nextliste.append(match)				
					
			self.status=TournamentStatus.Running
			Database.instance().setStatusTn(self.id, TournamentStatus.Running)
			self.currentRound=max([m.round for m in self.matchs])
						


	class Match():
		_roundnames = {1:'Final', 2:'Semi-finals', 3:'Quarter-finals'}
		def __init__(self, id, tour, round, t1, t2, p1, p2, KOtype=None):
			self.id = id
			self.tournament=tour
			self.round= round
			self.teams = [t1,t2]
			self.parents= [p1, p2]
			self.scores = list()
			self.played=False
			self.KOtype='W'

		def roundName(self):
			if self.round in Tournament.Match._roundnames.keys():
				return Tournament.Match._roundnames[self.round]
			else:
				return "Round of "+str(int(math.pow(2, self.round)))

		def playable(self):
			return self.round==self.tournament.currentRound

		#Returns winning team (Result='W') or losing Team (Result='L')
		def teamResult(self, result):
			if self.played:
				if result=='W':
					return self.teams[self.scores.index(max(self.scores))]
				elif result=='L':
					return self.teams[self.scores.index(min(self.scores))]
		

		@staticmethod
		def create(tour, round, side1, side2, KOtype=None):
			t1 = side1 if isinstance(side1, Team) else None
			p1 = side1 if not t1 else None
			t2 = side2 if isinstance(side2, Team) else None
			p2 = side2 if not t2 else None

			IDt1 = t1.id if t1 else None
			IDt2 = t2.id if t2 else None
			IDp1 = p1.id if p1 else None
			IDp2 = p2.id if p2 else None

			id = Database.instance().createMatchTn(tour.id, round, IDt1, IDt2, IDp1, IDp2, KOtype)
			return Tournament.Match(id, tour, round, t1, t2, p1, p2, KOtype)

		
		def setPlayed(self, start_time, duration, scores):
			if self.playable and not self.played:
				self.scores=scores
				self.played=True
				Database.instance().insertMatchTn(self.id, scores[0], scores[1], start_time, duration)
				self.tournament.updateTree()