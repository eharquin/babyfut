#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Adam SOIMANSOIB
"""
from babyfut_master.core.module import Module
from babyfut_master import modules


class MenuSwitch(object):
    def __init__(self, menu_module: Module):
        self.menu_module = menu_module

    def authQuickModule(self):
        self.menu_module.mainwin.connect_rfid()
        self.menu_module.switchModule(modules.AuthQuickModule)

    def tournamentModule(self):
        self.menu_module.switchModule(modules.TournamentModule)

    def leaderboardModule(self):
        self.menu_module.switchModule(modules.LeaderboardModule)

    def optionsModule(self):
        self.menu_module.switchModule(modules.OptionsModule)

    def privacyModule(self):
        self.menu_module.switchModule(modules.PrivacyModule)

    def editModule(self):
        self.menu_module.mainwin.connect_rfid()
        self.menu_module.switchModule(modules.EditModule)


class AutoQuickSwitch(object):
    def __init__(self, auto_quick_module: Module):
        self.auto_quick_module = auto_quick_module

    def cancel(self):
        self.auto_quick_module.mainwin.disconnect_rfid()
        self.auto_quick_module.switchModule(modules.MenuModule)

    def done(self):
        self.auto_quick_module.mainwin.disconnect_rfid()
        self.auto_quick_module.switchModule(modules.GameModule)


class EditSwitch(object):
    def __init__(self, edit_module: Module):
        self.edit_module = edit_module

    def back(self):
        self.edit_module.mainwin.disconnect_rfid()
        self.edit_module.switchModule(modules.MenuModule)


class PrivacySwitch(object):
    def __init__(self, privacy_module: Module):
        self.privacy_module = privacy_module

    def back(self):
        self.privacy_module.switchModule(modules.MenuModule)


class EndGameSwitch(object):
    def __init__(self, endgame_module: Module):
        self.endgame_module = endgame_module

    def back(self):
        self.endgame_module.switchModule(modules.MenuModule)

    def tournamentDisplay(self):
        self.endgame_module.switchModule(modules.TournamentDisplayModule)


class GameSwitch(object):
    def __init__(self, game_module: Module):
        self.game_module = game_module

    def cancel(self):
        self.game_module.switchModule(modules.MenuModule)

    def endgame(self):
        self.game_module.switchModule(modules.EndGameModule)


class LeaderboardSwitch(object):
    def __init__(self, leaderboard_module: Module):
        self.leaderboard_module = leaderboard_module

    def exit(self):
        self.leaderboard_module.switchModule(modules.MenuModule)


class OptionsSwitch(object):
    def __init__(self, options_module: Module):
        self.options_module = options_module

    def back(self):
        self.options_module.switchModule(modules.MenuModule)


class TournamentSwitch(object):
    def __init__(self, tournament_module: Module):
        self.tournament_module = tournament_module

    def participant_module(self):
        self.tournament_module.switchModule(modules.TournamentParticipantModule)

    def display_module(self):
        self.tournament_module.switchModule(modules.TournamentDisplayModule)

    def tournament_module(self):
        self.tournament_module.switchModule(modules.TournamentModule)

    def game_module(self):
        self.tournament_module.switchModule(modules.GameModule)

    def menu_module(self):
        self.tournament_module.switchModule(modules.MenuModule)
