#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtWidgets import QSizePolicy

from .auth import AuthModuleBase
from ..core.player import Side, PlayerGuest
from ..ui.authquick_ui import Ui_Form as AuthQuickWidget

class AuthQuickModule(AuthModuleBase):
	def __init__(self, parent):
		super().__init__(parent, AuthQuickWidget())

		self.smallPicSize = 200
		self.bigPicSize = 300
		self.leftSpacerWidth  = self.ui.widgetLayoutP1.layout().itemAt(0).spacerItem().geometry().width()
		self.rightSpacerWidth = self.ui.widgetLayoutP3.layout().itemAt(0).spacerItem().geometry().width()

	def load(self):
		logging.debug('Loading AuthQuickModule')
		super().load()

		for side in [Side.Left, Side.Right]:
			if len(self.players[side])==0:
				self.addPlayer(side, PlayerGuest)

		self.updateSides()

	def unload(self):
		logging.debug('Unloading AuthQuickModule')
		super().unload()
		#self.updateSides()

	def createPlayerList(self):
		self.players = {Side.Left: list(), Side.Right: list()}

	def addPlayer(self, side, player):
		# If there is a placeholder Guest, clear it from the list, we don't need it anymore
		if len(self.players[side])>0 and self.players[side][0]==PlayerGuest:
			self.players[side].clear()

		if len(self.players[side])<2:
			self.players[side].append(player)

			if len(self.players[Side.Left])>1 and len(self.players[Side.Right])>1:
				self.handleDone()
			else:
				self.updateSides()

	def updateSides(self):
		'''
		There might be issues with this function in the future:
		Unfortunatly, Qt does not allow naming spacers, we can only access them indirectly,
		via the layout's itemAt function. The problem with this approach is that if a spacer
		is for a reason or another placed out of order by pyuic5, this won't work. Take a look to
		ui/auth4p_ui.py to adapt if this ever occurs
		'''

		spacerLeft  = self.ui.widgetLayoutP1.layout().itemAt(0).spacerItem()
		spacerRight = self.ui.widgetLayoutP3.layout().itemAt(0).spacerItem()

		# Update Left P1
		if len(self.players[Side.Left])>0:
			self.players[Side.Left][0].displayImg(self.ui.imgP1)
			self.ui.lblP1.setText(self.players[Side.Left][0].name)
		else:
			PlayerGuest.displayImg(self.ui.imgP1)
			self.ui.lblP1.setText('')

		# Update Left P2
		if len(self.players[Side.Left])>1:
			self.ui.imgP1.setMaximumSize(self.smallPicSize, self.smallPicSize)
			self.players[Side.Left][1].displayImg(self.ui.imgP2)
			self.ui.lblP2.setText(self.players[Side.Left][1].name)
			self.ui.widgetLayoutP2.setVisible(True)
			spacerLeft.changeSize(self.leftSpacerWidth, spacerLeft.geometry().height(), QSizePolicy.Expanding, QSizePolicy.Expanding)
		else:
			self.ui.imgP1.setMaximumSize(self.bigPicSize, self.bigPicSize)
			PlayerGuest.displayImg(self.ui.imgP2)
			self.ui.lblP2.setText('')
			self.ui.widgetLayoutP2.setVisible(False)
			spacerLeft.changeSize(0, spacerLeft.geometry().height(), QSizePolicy.Ignored, QSizePolicy.Expanding)

		# Update Right P1
		if len(self.players[Side.Right])>0:
			self.players[Side.Right][0].displayImg(self.ui.imgP3)
			self.ui.lblP3.setText(self.players[Side.Right][0].name)
		else:
			PlayerGuest.displayImg(self.ui.imgP3)
			self.ui.lblP3.setText('')

		# Update Right P2
		if len(self.players[Side.Right])>1:
			self.ui.imgP3.setMaximumSize(self.smallPicSize, self.smallPicSize)
			self.players[Side.Right][1].displayImg(self.ui.imgP4)
			self.ui.lblP4.setText(self.players[Side.Right][1].name)
			self.ui.widgetLayoutP4.setVisible(True)
			spacerRight.changeSize(self.rightSpacerWidth, spacerRight.geometry().height(), QSizePolicy.Expanding, QSizePolicy.Expanding)
		else:
			self.ui.imgP3.setMaximumSize(self.bigPicSize, self.bigPicSize)
			PlayerGuest.displayImg(self.ui.imgP4)
			self.ui.lblP4.setText('')
			self.ui.widgetLayoutP4.setVisible(False)
			spacerRight.changeSize(0, spacerRight.geometry().height(), QSizePolicy.Ignored, QSizePolicy.Expanding)
