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

'''Different types of tournament. The value is the integer stored in the DB'''


class TournamentType(Enum):
    Elimination = 0
    Double = 1
    EliminationQualif = 2
    DoubleQualif = 3
    Qualif = 4


'''Different status of a tournament. The value is the integer stored in the DB'''


class TournamentStatus(Enum):
    Future = 0
    Running = 1
    Past = 2
    Cancelled = 3


'''Class for Tournament objects. Owns its team list and matchs list. 
Use static methode create to add a new one in DB.'''


class Tournament(QObject):

    def __init__(self, id, name, status, _type):
        QObject.__init__(self)
        self.id = id  # ID in DB
        self.name = name  # Name in DB
        self.status = status  # Enum TournamentStatus
        self.type = _type  # Enum TournamentType
        self.teams = list()  # List of Team Objects
        self.matchs = list()  # List of Tournament.Match Objects

        # Local use
        teamdict = dict()
        matchdict = dict()

        # Loads the Teams registered in the DB and appends them in the list
        for t in Database.instance().selectTeamsTn(self.id):
            players = [Player.loadFromDB(t[2])]
            if t[3]:
                players.append(Player.loadFromDB(t[3]))
            team = Team(t[0], t[1], players)
            teamdict[t[0]] = team
            self.teams.append(team)

        # Loads the Matches od the tournament in DB and appends them in the list with parent's ID
        for m in Database.instance().selectMatchsTn(self.id):
            t1 = teamdict[m[4]] if m[4] else None
            t2 = teamdict[m[6]] if m[6] else None
            match = Tournament.Match(m[0], self, m[8], t1, t2, m[10], m[11], m[9])
            if m[5] is not None and m[7] is not None:
                match.scores = [m[5], m[7]]
                match.played = True
            self.matchs.append(match)

        # Changes parent's ID to parent Match Object
        for m in self.matchs:
            matchdict[m.id] = m
        for m in self.matchs:
            m.parents[0] = matchdict[m.parents[0]] if m.parents[0] else None
            m.parents[1] = matchdict[m.parents[1]] if m.parents[1] else None

        # Finds the current Round of the tournament, if it's Running
        self.currentRound = max(
            [m.round for m in self.matchs if not m.played]) if self.status == TournamentStatus.Running else None

    '''Add a Team object to the tournament's team list'''

    def registerTeam(self, team):
        if self.status == TournamentStatus.Future:
            self.teams.append(team)
            Database.instance().registerTeamTn(team.id, self.id)

    '''If running, updates every Tree game with the known teams. Called everytime a new game is played
	Updates the currentRound when all games of a round are played.
	Updates the status to Past when all games are played'''

    def updateTree(self):
        if self.status == TournamentStatus.Running:
            for match in self.matchs:
                modified = False
                for i in [0, 1]:
                    if match.teams[i] is None and match.parents[i] and match.parents[i].played:
                        match.teams[i] = match.parents[i].teamResult(match.KOtype[i])
                        modified = True
                if modified:
                    t1 = match.teams[0].id if match.teams[0] else None
                    t2 = match.teams[1].id if match.teams[1] else None
                    Database.instance().updateTreeMatchTn(match.id, t1, t2)
            if all(m.played for m in self.matchs if m.playable()):
                self.currentRound -= 1
                if self.currentRound == 0:
                    self.status = TournamentStatus.Past
                    Database.instance().setStatusTn(self.id, self.status)

    '''Returs a dict where keys are Rounds number and values are the list of the Round's matchs'''

    @property
    def rounds(self):
        rounds = dict(list())
        for m in self.matchs:
            if m.roundName() in rounds.keys():
                rounds[m.roundName()].append(m)
            else:
                rounds[m.roundName()] = [m]
        return rounds

    '''Creates and return a list of all Tournament Objects in the DB'''

    @staticmethod
    def selectAll(status=None):
        if status:
            status = status.value
        return [Tournament(int(t[0]), t[1], TournamentStatus(int(t[2])), TournamentType(int(t[3]))) for t in
                Database.instance().selectAllTn(status)]

    '''Inserts a tournament in DB and returns the Tournament Object corresponding'''

    @staticmethod
    def create(name, _type):
        id = Database.instance().createTn(name, _type.value)
        return Tournament(id, name, TournamentStatus.Future, _type)

    '''Closes registration of a tournament in status Future and generates all matchs.
	Sets status to running.
	Type Elimination implemented, /TODO other types are to implement.'''

    def validate(self):
        if self.status == TournamentStatus.Future:
            if self.type == TournamentType.Elimination:
               self.singleElimination()
            elif self.type == TournamentType.doubleElimination:
                self.doubleElimination()

            self.status = TournamentStatus.Running
            Database.instance().setStatusTn(self.id, TournamentStatus.Running)
            self.currentRound = max([m.round for m in self.matchs])

    def singleElimination(self):
        # Initiate a list containing all the teams
        team_list = self.teams
        # Initiate another list that contains the list of parent matches for the next round
        next_round_parent_matches = list()
        # Initiate an int equal to the number of teams.
        teams_count = len(team_list)
        # Initiate an int equal to the number of rounds, based on the number of teams.
        rounds_count = math.floor(math.log2(teams_count))
        # Initiate an int equal to the number of supplementary matches that have to be played when the teams_count is not a power of 2
        additional_matches_count = int(teams_count - math.pow(2, rounds_count))

        # First, build the additional matches (there are no additional matches when teams_count is a power of 2).
        for i in range(additional_matches_count):
            # Chose two teams from the available list.
            t1 = choice(team_list)
            team_list.remove(t1)
            t2 = choice(team_list)
            team_list.remove(t2)
            # Insert the Match into the database
            match = Tournament.Match.create(self, int(rounds_count + 1), t1, t2, ['W', 'W'])
            # Add the match to the list of the parents for next round
            next_round_parent_matches.append(match)
            # Also add it to the Tournament's matches list
            self.matchs.append(match)
        # Add the remaining teams to the list for the next round
        next_round_parent_matches += team_list

        # Then, build each round one by one
        for round_number in range(rounds_count, 0, -1):
            # Make a copy of the list of the available teams for the round
            team_list = next_round_parent_matches.copy()
            next_round_parent_matches.clear()
            # Create each match from the round
            for j in range(0, int(pow(2, round_number - 1))):
                # Chose two teams from the available list.
                t1 = choice(team_list)
                team_list.remove(t1)
                t2 = choice(team_list)
                team_list.remove(t2)
                # Insert the Match into the database
                match = Tournament.Match.create(self, int(round_number), t1, t2, ['W', 'W'])
                # Add the match to the list of the parents for next round
                next_round_parent_matches.append(match)
                # Also add it to the Tournament's matches list
                self.matchs.append(match)

    def doubleElimination(self):
        # Initiate a list containing all the teams
        team_list = self.teams
        # Initiate 2 other lists that contains the list of parent matches for the next round :
        # From a WB round to another
        next_round_parent_matches = list()
        # From a LB round to the second LB round of the current tournament's round
        parent_matches_for_second_loser_round = list()
        # From a LB round to next tournament's round
        next_loser_round_parent_matches = list()
        # Initiate an int equal to the number of teams.
        teams_count = len(team_list)
        # Initiate an int equal to the number of rounds, based on the number of teams.
        rounds_count = math.floor(math.log2(teams_count))
        # Initiate an int equal to the number of supplementary matches that have to be played when the teams_count is not a power of 2
        additional_matches_count = int(teams_count - math.pow(2, rounds_count))

        # First, build the additional matches (there are no additional matches when teams_count is a power of 2).
        for i in range(additional_matches_count):
            # Chose two teams from the available list.
            t1 = choice(team_list)
            team_list.remove(t1)
            t2 = choice(team_list)
            team_list.remove(t2)
            # Insert the Match into the database
            match = Tournament.Match.create(self, int(rounds_count + 1), t1, t2, ['W', 'W'])
            # Add the match to the list of the parents for next round
            next_round_parent_matches.append(match)
            # Also add it to the Tournament's matches list
            self.matchs.append(match)
        # Add the remaining teams to the list for the next round
        next_round_parent_matches += team_list

        # Then, build each round one by one
        for round_number in range(rounds_count, 0, -1):
            # Make a copy of the list of the available teams for the round
            team_list = next_round_parent_matches.copy()
            next_round_parent_matches.clear()
            # Create each match from the round

            # Winner Bracket
            for j in range(0, int(pow(2, round_number - 1))):
                # Chose two teams from the available list.
                t1 = choice(team_list)
                team_list.remove(t1)
                t2 = choice(team_list)
                team_list.remove(t2)
                # The match corresponds to the winners of the previous round
                # Insert the Match into the database
                match = Tournament.Match.create(self, int(round_number), t1, t2, ['W', 'W'])
                # Add the match to the list of the parents for next round
                next_round_parent_matches.append(match)
                # Also add it to the Tournament's matches list
                self.matchs.append(match)

            # Loser Bracket
            for j in range(0, int(pow(2, round_number - 2))):
                # If it's the first round, it requires two losers from the winner bracket
                if round_number == rounds_count:
                    # Copy the list of the matches from the winner bracket round that was just played
                    teams_from_winner_list = next_round_parent_matches.copy()
                    # Chose two teams from the available list.
                    t1 = choice(teams_from_winner_list)
                    teams_from_winner_list.remove(t1)
                    t2 = choice(teams_from_winner_list)
                    teams_from_winner_list.remove(t2)

                    # Insert the Match into the database
                    match = Tournament.Match.create(self, int(round_number), t1, t2, ['L', 'L'])
                    # Add the match to the list of the parents for next round
                    next_loser_round_parent_matches.append(match)
                    # Also add it to the Tournament's matches list
                    self.matchs.append(match)

                # If it's the last round, there will only be one round in Loser Bracket
                else:
                    # Copy the list of the matches from the winner bracket round that was just played
                    teams_from_winner_list = next_round_parent_matches.copy()
                    teams_from_loser_list = next_loser_round_parent_matches.copy()
                    next_loser_round_parent_matches.clear()
                    # Chose a team from the Winner Bracket
                    t1 = choice(teams_from_winner_list)
                    teams_from_winner_list.remove(t1)
                    # Chose another one from the Loser Bracket
                    t2 = choice(teams_from_loser_list)
                    teams_from_loser_list.remove(t2)

                    # Insert the Match into the database
                    match = Tournament.Match.create(self, int(round_number), t1, t2, ['L', 'W'])
                    # Add the match to the list of the parents for next round
                    parent_matches_for_second_loser_round.append(match)
                    # Also add it to the Tournament's matches list
                    self.matchs.append(match)

                    # If it isn't the last round, a second LB round is required between two winners from the LB
                    if round_number == 1:
                        # Copy the list of the matches from the loser bracket round that was just played
                        teams_from_loser_list = parent_matches_for_second_loser_round.copy()
                        parent_matches_for_second_loser_round.clear()
                        # Chose a team from the Winner Bracket
                        t1 = choice(teams_from_loser_list)
                        teams_from_loser_list.remove(t1)
                        # Chose another one from the Loser Bracket
                        t2 = choice(teams_from_loser_list)
                        teams_from_loser_list.remove(t2)

                        # Insert the Match into the database
                        match = Tournament.Match.create(self, int(round_number), t1, t2, ['W', 'W'])
                        # Add the match to the list of the parents for next round
                        next_loser_round_parent_matches.append(match)
                        # Also add it to the Tournament's matches list
                        self.matchs.append(match)

        # In the end, we only have one team in "next_round_parents" and "next_loser_round_parents"
        # Create a last match which will be the great final between these two teams.
        # Copy the list of the matches from the winner bracket round that was just played
        next_loser_round_parent_matches.clear()
        # Chose a team from the Winner Bracket
        t1 = choice(next_round_parent_matches)
        # Chose another one from the Loser Bracket
        t2 = choice(next_loser_round_parent_matches)

        # Insert the Match into the database
        match = Tournament.Match.create(self, 0, t1, t2, ['W', 'W'])
        # Add the match to the list of the parents for next round
        next_loser_round_parent_matches.append(match)
        # Also add it to the Tournament's matches list
        self.matchs.append(match)

    '''Class in the Tournament Namespace to handle Tournament Matchs
	Use method create to insert a new one in the DB'''

    class Match:
        # Special rounds names
        _roundnames = {0: 'Great Final', 1: 'Final', 2: 'Semi-finals', 3: 'Quarter-finals'}

        def __init__(self, id, tour, round, t1, t2, p1, p2, k1='W', k2='W'):
            self.id = id  # ID in DB
            self.tournament = tour  # Tournament Object
            self.round = round  # Round number
            self.teams = [t1, t2]  # list of 2 Team Objects: None if the team is not known yet
            self.parents = [p1, p2]  # list of 2 Tournament.Match object, None if has no parent
            self.scores = list()  # list of 2 scores, empty if not played. Same order as teams list.
            self.played = False
            self.KOtype = [k1, k2]  # List of 2 strings which are 'W' if the corresponding team is the winner of the parent match, 'L' if it is the loser

        '''Returns the Round name : "Round of ..." or special round name'''

        def roundName(self):
            if self.round in Tournament.Match._roundnames.keys():
                return Tournament.Match._roundnames[self.round]
            else:
                return "Round of " + str(int(math.pow(2, self.round)))

        '''Match is playable if its round is the Tournament CurrentRound'''

        def playable(self):
            return self.round == self.tournament.currentRound

        '''If played, returns winning team (Result='W') or losing Team (Result='L')'''

        def teamResult(self, result):
            if self.played:
                if result == 'W':
                    return self.teams[self.scores.index(max(self.scores))]
                elif result == 'L':
                    return self.teams[self.scores.index(min(self.scores))]

        '''Inserts of Match in DB and returns Match object corresponding'''

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

        '''Updates scores and time in DB, and sets it played'''

        def setPlayed(self, start_time, duration, scores):
            if self.playable and not self.played:
                self.scores = scores
                self.played = True
                Database.instance().insertMatchTn(self.id, scores[0], scores[1], start_time, duration)
                self.tournament.updateTree()
