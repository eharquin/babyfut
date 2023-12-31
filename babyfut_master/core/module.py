#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modif : Yoann Malot, Thibaud Le Graverend
"""

import logging

from PyQt5.QtWidgets import QApplication, QWidget

'''
Abstract class, parent of every Module if folder modules. Herits from a QWidget and is shown in the MainWindow's StackedWidget.
Its ui attribute is the UI class generated by Qt Designer.
Handles sending messages between modules, and switching from one to another.
'''
class Module(QWidget):
	def __init__(self, parent, widget):
		# UI Setup
		QWidget.__init__(self, parent)
		self.mainwin = parent
		self.ui = widget
		self.ui.setupUi(self)

	'''Unloads the current module, loads the one of the type in parameter and shows it'''
	def switchModule(self, new_type):
		curmod_idx = self.mainwin.findMod(type(self))
		newmod_idx = self.mainwin.findMod(new_type)

		if curmod_idx<0:
			logging.error('Unknown panel {}'.format(type(self)))
		elif newmod_idx<0:
			logging.error('Unknown panel {}'.format(new_type))
		else:
			# Unfocus the current module
			if QApplication.focusWidget() != None:
				QApplication.focusWidget().clearFocus()

			# Swap modules by unloading, changing the ui then loading
			self.mainwin.modules[curmod_idx].unload()
			self.mainwin.ui.panels.setCurrentIndex(newmod_idx)
			self.mainwin.ui.panels.setFocusProxy(self.mainwin.modules[newmod_idx])
			self.mainwin.modules[newmod_idx].setFocus()

			# Select first element of the Module
			self.mainwin.modules[newmod_idx].focusNextChild()
			self.mainwin.modules[newmod_idx].focusPreviousChild()
			self.mainwin.modules[newmod_idx].ui.retranslateUi(self.mainwin)
			self.mainwin.modules[newmod_idx].load()
			self.mainwin.setWindowTitle('Babyfut')

	'''Calls method other of the module of given type, with the given parameter.
	Allows to send data from a module to another before switching.'''
	def send(self, to, **kwargs):
		mod_idx = self.mainwin.findMod(to)

		if mod_idx<0:
			logging.error('Unknown panel {}'.format(to))
		else:
			self.mainwin.modules[mod_idx].other(**kwargs)

	'''Virtual method, called for each module before being shown'''
	def load(self):
		logging.warning('Unimplemented method "load" for {}'.format(self.__class__))

	'''Virtual method, called for each module before being replaced'''
	def unload(self):
		logging.warning('Unimplemented method "unload" for {}'.format(self.__class__))

	'''Virtual method, acts like a message receiver for each module.'''
	def other(self, **kwargs):
		logging.warning('Unimplemented method "other" for {}'.format(self.__class__))
