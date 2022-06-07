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


class AutoQuickSwitch(object):
    def __init__(self, auto_quick_module: Module):
        self.auto_quick_module = auto_quick_module

    def cancel(self):
        self.auto_quick_module.mainwin.disconnect_rfid()
        self.auto_quick_module.switchModule(modules.MenuModule)

    def done(self):
        self.auto_quick_module.switchModule(modules.GameModule)


class EditSwitch(object):
    def __init__(self, edit_module: Module):
        self.edit_module = edit_module

    def back(self):
        self.edit_module.mainwin.disconnect_rfid()
        self.edit_module.switchModule(modules.MenuModule)
