#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging

from PyQt5.QtCore import Qt, QCoreApplication

from Babyfut import modules
from Babyfut.core.module import Module
from Babyfut.ui.privacy_ui import Ui_Form as PrivacyWidget

class PrivacyModule(Module):
	def __init__(self, parent):
		super().__init__(parent, PrivacyWidget())
		self.ui.txtPrivacy.setHtml('''<p>
		Babyf’UT est un traitement opéré par l’UTC dans le cadre d’un projet étudiant au Fablab. Il a pour finalités le suivi de la participation des inscrits, l’organisation de tournois, l’établissement de classements et statistiques relatives aux scores du joueur et à son temps passé à jouer.
La base légale du traitement est le consentement (article 6 du règlement européen 2016/679, dit RGPD).
Les données traitées sont vos nom, prénom, login, statut (étudiant, professeur, ...), identifiant de badge, photo ainsi que les informations relatives aux parties (score, temps passé, coéquipiers, adversaires…) que vous aurez disputées.
Ces données seront accessibles par tous, sauf l’identifiant du badge qui ne sera accessible qu’aux administrateurs du logiciel.
<br/>
Si vous clôturez votre compte, les données personnelles vous concernant seront supprimées. Ne seront conservées que des données anonymes relatives aux parties que vous aurez disputées.
Votre compte Babyf’UT sera automatiquement clôturé au moment de la clôture de votre compte UTC et les données personnelles vous concernant seront supprimées dans Babyf’UT. Ne seront conservées que des données anonymes relatives aux parties que vous aurez disputées.
<br/>
Conformément au règlement européen 2016/679 dit RGPD, vous pouvez retirer votre consentement à tout moment et demander l’effacement des données vous concernant. Vous disposez également d’un droit d’accès, de rectification et d’opposition aux informations qui vous concernent ainsi qu’un droit à la limitation du traitement de ces données, droits que vous pouvez exercer en vous adressant à dpo@utc.fr.
Si vous estimez, après nous avoir contactés, que vos droits sur vos données ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL.
		</p>''')

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
