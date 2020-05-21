#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann MALOT, Thibaud LE GRAVEREND
"""

from PyQt5.QtCore import QObject

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
	Passed = 2
	Cancelled = 3

class Tournament(QObject):

	def __init__(self, id, name, status, _type):
		QObject.__init__(self)
		self.id = id
		self.name = name
		self.status = status
		self.type = _type
		self.teams = [Team(t[0], t[1], [t[2], t[3]]) for t in Database.instance().selectTeamsTn(self.id)]
        self.matchs = list()

	def registerTeam(self, team):
		if self.status == TournamentStatus.Future:
			self.teams.append(team)
			Database.instance().registerTeamTn(team.id, self.id)
	
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
			if self.type==TournamentType.Elimination:
				nbteams = len(liste)
				nbrounds = math.floor(math.log2(nbteams))
				nbsupmatchs = nbteams-math.pow(2,nbrounds)
				supmatchs = list()
				for i in range(nbsupmatchs):
					t1 = choice(liste)
					liste.remove(t1)
					t2 = choice(liste)
					liste.remove(t2)
					match = Match.create(self, nbrounds+1, t1, t2)
					liste.append(match)
					self.matchs.append(match)

				for round in range(0, nbrounds):
					for j in range(0, pow(2, round-1)):
						t1=choice(liste)
						liste.remove(t1)
						t2=choice(liste)
						liste.remove(t2)
						self.matchs.append(Match.create(tour,round, t1, t2 ))
						


	class Match():
		def __init__(tour, round, t1, t2, p1, p2, KOtype=None):
			self.tournament=tour
			self.round=round
			self.team1 = t1
			self.team2 = t2
			self.parent1=p1
			self.parent2=p2
			
		
		@staticmethod
		def create(tour, round, side1, side2, KOtype=None):
			t1 = side1 if isinstance(side1, Team) else None
			p1 = side1 if not t1 else None
			t2 = side2 if isinstance(side2, Team) else None
			p2 = side2 if not t2 else None
			return Match(tour, round, t1, t2, p1, p2, KOtype)




		def setTeams():
			pass
		
		def setPlayed(timestamps, duration, score1,  score2):
			pass
