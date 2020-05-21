#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann MALOT, Thibaud LE GRAVEREND
"""

from PyQt5.QtCore import QObject

from .database import Database, DatabaseError
from .team import Team
from enum import Enum

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
        # self.matchs = matchlist

	def registerTeam(self, team):
		if self.status == TournamentStatus.Future:
			self.teams.append(team)
			Database.instance().registerTeamTn(team.id, self.id)
	
	@staticmethod
	def selectAll(status=None):
		return [Tournament(int(t[0]), t[1], TournamentStatus(int(t[2])), TournamentType(int(t[3]))) for t in Database.instance().selectAllTn(status)]

	@staticmethod
	def create(name, _type):
		id = Database.instance().createTn(name, _type.value)
		return Tournament(id, name, TournamentStatus.Future, _type)