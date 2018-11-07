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

class Module(QtWidgets.QWidget):
	def __init__(self, parent, widget):
		# UI Setup
		QtWidgets.QWidget.__init__(self, parent)
		self.mainwin = parent
		self.ui = widget
		self.ui.setupUi(self)
	
	def switchModule(self, new_type):
		curmod_idx = self.mainwin.findMod(type(self))
		newmod_idx = self.mainwin.findMod(new_type)
		
		if curmod_idx<0:
			logging.error('Unknown panel {}'.format(type(self)))
		elif newmod_idx<0:
			logging.error('Unknown panel {}'.format(new_type))
		else:
			# Unfocus the current module
			if QApplication.focusWidget() != None:
				QApplication.focusWidget().clearFocus()
			
			# Swap modules by unloading, changing the ui then loading
			self.mainwin.modules[curmod_idx].unload()
			self.mainwin.ui.panels.setCurrentIndex(newmod_idx)
			self.mainwin.ui.panels.setFocusProxy(self.mainwin.modules[newmod_idx])
			self.mainwin.modules[newmod_idx].setFocus()
			
			# Select first element of the Module
			self.mainwin.modules[newmod_idx].focusNextChild()
			self.mainwin.modules[newmod_idx].focusPreviousChild()
			self.mainwin.modules[newmod_idx].load()

	def send(self, to, **kwargs):
		mod_idx = self.mainwin.findMod(to)
		
		if mod_idx<0:
			logging.error('Unknown panel {}'.format(to))
		else:
			self.mainwin.modules[mod_idx].other(**kwargs)
	
	def load(self):
		logging.warning('Unimplemented method "load" for {}'.format(self.__class__))

	def unload(self):
		logging.warning('Unimplemented method "unload" for {}'.format(self.__class__))

	def other(self, **kwargs):
		logging.warning('Unimplemented method "other" for {}'.format(self.__class__))
