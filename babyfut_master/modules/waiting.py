#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Kumarasamy Yaathavan, Gaillochet Claire, Soimansoib Adam
"""

import logging

from PyQt5.QtCore import Qt, QCoreApplication
from ..ui.waiting_ui import Ui_Form as WaitingWidget

from ..core.module import Module

class WaitingModule(Module):
    def __init__(self, parent):
        super().__init__(parent, WaitingWidget())

    def load(self):
        logging.debug('Loading WaitingModule')

    def unload(self):
        logging.debug('Unloading WaitingModule')

    def other(self, **kwargs):
        logging.debug('Other WaitingModule')