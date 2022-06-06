#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Adam SOIMANSOIB
"""
from babyfut_master.core.module import Module
from babyfut_master import modules


class MenuSwitch(object):
    def __init__(self, parent: Module):
        self.parent = parent

    def authQuickModule(self):
        # TODO: Add RFID and Goal Signals connection
        self.parent.switchModule(modules.AuthQuickModule)

    def tournamentModule(self):
        self.parent.switchModule(modules.TournamentModule)

    def leaderboardModule(self):
        self.parent.switchModule(modules.LeaderboardModule)

    def optionsModule(self):
        self.parent.switchModule(modules.OptionsModule)

    def privacyModule(self):
        self.parent.switchModule(modules.PrivacyModule)

    def editModule(self):
        self.parent.switchModule(modules.EditModule)
