#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Adam SOIMANSOIB
"""
from babyfut_master.core.module import Module
from babyfut_master import modules


class MenuSwitch(object):
    def __init__(self, menuModule: Module):
        self.menuModule = menuModule

    def authQuickModule(self):
        self.menuModule.mainwin.connect_rfid()
        self.menuModule.switchModule(modules.AuthQuickModule)

    def tournamentModule(self):
        self.menuModule.switchModule(modules.TournamentModule)

    def leaderboardModule(self):
        self.menuModule.switchModule(modules.LeaderboardModule)

    def optionsModule(self):
        self.menuModule.switchModule(modules.OptionsModule)

    def privacyModule(self):
        self.menuModule.switchModule(modules.PrivacyModule)

    def editModule(self):
        self.menuModule.mainwin.connect_rfid()
        self.menuModule.switchModule(modules.EditModule)
