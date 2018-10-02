#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QApplication

from modules import *

class Module(QtWidgets.QWidget):
	def __init__(self, parent=None, widget=None):
		# UI Setup
		QtWidgets.QWidget.__init__(self, parent)
		self.parent_win = parent
		self.ui = widget
		self.ui.setupUi(self)

	def switchModule(self, new_type):
		panel_idx = self.parent_win.modules.index(new_type)
		
		if panel_idx<0:
			logging.error('Error: unknown panel {}'.format(new_type))
		else:
			self.parent_win.ui.panels.currentWidget().releaseKeyboard()
			if QApplication.focusWidget() != None:
				QApplication.focusWidget().clearFocus()
			self.parent_win.ui.panels.currentWidget().unload()
			
			self.parent_win.ui.panels.setCurrentIndex(panel_idx)
			
			self.parent_win.ui.panels.currentWidget().load()
			# Select first element of the Module
			self.parent_win.ui.panels.currentWidget().focusNextChild()
			self.parent_win.ui.panels.currentWidget().focusPreviousChild()
			self.parent_win.ui.panels.currentWidget().grabKeyboard()

	def load(self):
		logging.warning('Unimplemented method "load" for {}'.format(self.__class__))

	def unload(self):
		logging.warning('Unimplemented method "unload" for {}'.format(self.__class__))

	def other(self, **kwargs):
		logging.warning('Unimplemented method "other" for {}'.format(self.__class__))
