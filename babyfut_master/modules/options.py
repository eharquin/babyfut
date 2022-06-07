#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs : Yoann Malot, Thibaud Le Graverend
"""

import logging

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QRadioButton, QSlider

from .. import modules
from common.settings import Settings
from common.module_switch import OptionsSwitch
from ..core.module import Module
from ..ui.options_ui import Ui_Form as OptionsWidget

class OptionsModule(Module):
	def __init__(self, parent):
		super().__init__(parent, OptionsWidget())
		self.ui.sliderGameOverValue.valueChanged.connect(self.updateGameOverLabel)
		self.ui.rbGameOver_Score.clicked.connect(self.updateGameOverLabel)
		self.ui.rbGameOver_Time.clicked.connect(self.updateGameOverLabel)

		self.ui.sliderGameOverValue.installEventFilter(self)

	def load(self):
		logging.debug('Loading OptionsModule')

		# Set Gameover condition from settings
		self.ui.rbGameOver_Score.setChecked(Settings['gameover.type']=='score')
		self.ui.rbGameOver_Time.setChecked(Settings['gameover.type']=='time')
		self.ui.sliderGameOverValue.setValue(Settings['gameover.value'])

		# Set League players from settings
		self.ui.rbNumPlayerLeague_1.setChecked(Settings['league.playerPerTeam']==1)
		self.ui.rbNumPlayerLeague_2.setChecked(Settings['league.playerPerTeam']==2)

		# Set Language from settings
		self.ui.rbLanguage_English.setChecked(Settings['ui.language']=='en')
		self.ui.rbLanguage_French.setChecked(Settings['ui.language']=='fr')

		self.selectIndex = 0
		self.updateSelection()
		self.updateGameOverLabel(0)

	def unload(self):
		logging.debug('Unloading OptionsModule')

	def other(self, **kwargs):
		logging.debug('Other OptionsModule')

	def eventFilter(self, obj, event):
		if obj==self.ui.sliderGameOverValue and event.type()==QEvent.KeyPress and (event.key()==Qt.Key_Up or event.key()==Qt.Key_Down):
			self.keyPressEvent(event)
			return True

		return False

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

		elif e.key() == Qt.Key_Return:
			self.handleSave()

		elif e.key() == Qt.Key_Up:
			#self.parent().focusPreviousChild()
			self.selectIndex = self.selectIndex-1 if self.selectIndex!=0 else len(self.selectables)-1
			self.updateSelection()

		elif e.key() == Qt.Key_Down:
			#self.parent().focusNextChild()
			self.selectIndex = self.selectIndex+1 if self.selectIndex!=len(self.selectables)-1 else 0
			self.updateSelection()

	def updateSelection(self):
		self.selectables = []
		isSelectable = lambda widget: (isinstance(widget, QRadioButton) and widget.isChecked()) or isinstance(widget, QSlider)

		for gb in [self.ui.gbGameOver, self.ui.gbLeaguePlayers, self.ui.gbLanguage]:
			self.selectables.extend([child for child in gb.children() if isSelectable(child)])

		self.selectables[self.selectIndex].setFocus()

	def updateGameOverLabel(self, val):
		sliderVal = self.ui.sliderGameOverValue.value()
		strPoints = '{} point{}'.format(sliderVal, 's' if sliderVal>1 else '')
		strTime = '{} minute{}'.format(sliderVal, 's' if sliderVal>1 else '')
		self.ui.lblGameOverValue.setText(strPoints if self.ui.rbGameOver_Score.isChecked() else strTime)

	def handleSave(self):
		Settings['ui.language'] = 'en' if self.ui.rbLanguage_English.isChecked() else 'fr'
		Settings['gameover.type'] = 'score' if self.ui.rbGameOver_Score.isChecked() else 'time'
		Settings['gameover.value'] = self.ui.sliderGameOverValue.value()
		Settings['league.playerPerTeam'] = 1 if self.ui.rbNumPlayerLeague_1.isChecked() else 2
		Settings.saveSettingsToJSON()
		self.mainwin._loadSettings()
		OptionsSwitch(self).back()

	def handleBack(self):
		OptionsSwitch(self).back()
