#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import Qt, QCoreApplication

from module import Module
import modules
from ui.privacy_ui import Ui_Form as PrivacyWidget

class PrivacyModule(Module):
	def __init__(self, parent):
		super().__init__(parent, PrivacyWidget())
		self.ui.txtPrivacy.setHtml(QCoreApplication.translate('consent', '''<p>
		This software uses personnal information in accordance to GDPR, such as:
		<ul>
			<li>Your Name and Surname</li>
			<li>Your Picture (if public)</li>
			<li>...</li>
		</ul>
		</p> 

		<p>
		That way players can keep track of their score and compare it with others.
		<br/>
		yada yada
		</p>'''))

	def load(self):
		logging.debug('Loading PrivacyModule')

	def unload(self):
		logging.debug('Unloading PrivacyModule')
	
	def other(self, **kwargs):
		logging.debug('Other PrivacyModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()
		
		super().keyPressEvent(e)
			
	def handleBack(self):
		self.switchModule(modules.MenuModule)
