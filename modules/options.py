#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QApplication

from settings import Settings
from module import Module
import modules
from ui.options_ui import Ui_Form as OptionsWidget

class OptionsModule(Module):
	def __init__(self, parent):
		super().__init__(parent, OptionsWidget())

		# Button connections
		self.ui.btnSave.clicked.connect(self.handleSave)
		self.ui.btnBack.clicked.connect(self.handleBack)

	def load(self):
		logging.debug('Loading OptionsModule')
		cbb = QComboBox()
		cbb.addItem('true')
		cbb.addItem('false')
		self.ui.options.insertRow(self.ui.options.rowCount())
		self.ui.options.setItem(self.ui.options.rowCount()-1, 0, QTableWidgetItem('FullScreen'))
		self.ui.options.setCellWidget(self.ui.options.rowCount()-1, 1, cbb)

	def unload(self):
		logging.debug('Unloading OptionsModule')
		# Delete the table's content
		self.ui.options.setRowCount(0)
	
	def other(self, **kwargs):
		logging.debug('Other OptionsModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()
		elif e.key() == Qt.Key_Return:
			self.handleSave()

	def handleSave(self):
		Settings['ui.fullscreen'] = self.ui.options.cellWidget(0, 1).currentText().lower() == 'true'
		self.mainwin._refreshAfterSettings()
		self.switchModule(modules.MenuModule)

	def handleBack(self):
		# ToDo: Maybe add a warning
		self.switchModule(modules.MenuModule)
