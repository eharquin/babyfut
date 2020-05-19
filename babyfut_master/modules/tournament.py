#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend
"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *

from ..core.module import Module
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent, QSignalMapper
from PyQt5.QtGui import QFont

from ..core.database import Database
from ..core.tournament import Tournament, TournamentStatus

from .. import modules
from ..ui.authleague_ui import Ui_Form as TournamentWidget
from ..ui.create_tournament_dialog_ui import Ui_Dialog as CreateTournamentDialog
from ..ui.tournamentlist_ui import Ui_Form as TournamentListWidget
from ..ui.tournamentparticipant_ui import Ui_Form as TournamentParticipantWidget



class TournamentListItem(QWidget):
	def __init__(self, parent, tournament):
		QWidget.__init__(self, parent)
		self.tournament = tournament
		self.ui = TournamentListWidget()
		self.ui.setupUi(self)
		self.ui.tnName.setText(tournament.name)
		self.ui.tnStatus.setText(self.ui.tnStatus.text().format(tournament.status.name))
		self.ui.tnType.setText(self.ui.tnType.text().format(tournament.type.name))
		self.ui.btnDelete.clicked.connect(self.deleteTn)

	def deleteTn(self):
		# Need to print a QDialog and then delete
		pass


class TournamentModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentWidget())
		self.parent = parent
		self.ui.btnCreate.clicked.connect(self.createTournament)
		self.ui.btnGo.clicked.connect(self.selectTn)

	def load(self):
		logging.debug('Loading TournamentModule')
		self.loadTournaments()


	def unload(self):
		logging.debug('Loading TournamentModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.MenuModule)

	def createTournament(self):
		dialog = CreateDialog(self.parent)
		dialog.exec()

	def loadTournaments(self):
		self.ui.tournamentList.clear()
		tournaments = Tournament.selectAll()
		for tournament in tournaments:
			item = QListWidgetItem()
			tnWidget = TournamentListItem(self.ui.tournamentList,tournament)
			item.setSizeHint(tnWidget.size())
			self.ui.tournamentList.addItem(item)
			self.ui.tournamentList.setItemWidget(item, tnWidget)

	def selectTn(self):
		tn = self.ui.tournamentList.itemWidget(self.ui.tournamentList.currentItem()).tournament
		if tn.status==TournamentStatus.Future:
			# Display player list
			self.switchModule(modules.TournamentParticipantModule)
			pass
		if tn.status==TournamentStatus.Running:
			# Display tournament
			pass
		if tn.status==TournamentStatus.Passed:
			# Display tournament table and results
			pass

	def unloadTournaments():
		pass

class TournamentParticipantModule(Module):
	def __init__(self, parent):
		super().__init__(parent, TournamentParticipantWidget())
		self.parent = parent


	def load(self):
		logging.debug('Loading TournamentModule')
		#self.loadTournaments()


	def unload(self):
		logging.debug('Loading TournamentModule')

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.handleBack()

	def handleBack(self):
		self.switchModule(modules.MenuModule)

class CreateDialog(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.parent=parent
		self.ui = CreateTournamentDialog()
		self.ui.setupUi(self)
		self.setWindowTitle('Create a tournament')
		self.keyboard = KeyboardWidget(self)
		self.keyboard.hide()
		
		self.ui.editName.clicked.connect(self.keyboard.show)
		self.ui.enter.clicked.connect(lambda : self.createTournament(self.ui.nameInput.text(), self.ui.typeTn.currentIndex()))


	# May handle other options in the future
	def createTournament(self, name, typeTn):
		db = Database.instance()
		db.createTn(name, typeTn)

	def finish(self):
		self.done(1)
		

class KeyboardWidget(QWidget):
	def __init__(self, parent):
		super(KeyboardWidget, self).__init__(parent)
		self.parent = parent
		self.signalMapper = QSignalMapper(self)
		self.signalMapper.mapped[int].connect(self.buttonClicked)
		self.setGeometry(0, 0, parent.width(), parent.height())
		self.initUI()

	def initUI(self):
		self.verticalLayout = QVBoxLayout()
		self.layout = QGridLayout()

		self.title = QLabel("What's the tournament's name ?")
		self.title.setFont(QFont('Arial', 25))
		self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter)

		self.setAutoFillBackground(True)
		self.text_box = QLineEdit()
		self.text_box.setReadOnly(True)
		self.text_box.setMaxLength(30)
		self.text_box.setFont(QFont('Arial', 20))

		self.verticalLayout.addWidget(self.text_box)

		self.maj = True
		self.namesMaj = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
						'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
						'Q', 'S', 'D','F', 'G', 'H', 'J', 'K', 'L', 'M', 
						'W', 'X', 'C', 'V', 'B', 'N', '?', '!', '.', '-']
		
		self.namesMin =  ['é', 'è', 'à', 'ç', '(', ')', '[', ']', '_', '@',
						'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
						'q', 's', 'd','f', 'g', 'h', 'j', 'k', 'l', 'm',
						'w', 'x', 'c', 'v', 'b', 'n',"'",';',':','/']

		self.positions = [(i, j) for i in range(4) for j in range(10)]

		for position, name in zip(self.positions, self.namesMaj):

			if name == '':
				continue
			button = QPushButton(name)
			button.setFont(QFont('Arial', 20))
			button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			button.KEY_CHAR = ord(name)
			button.clicked.connect(self.signalMapper.map)
			self.signalMapper.setMapping(button, button.KEY_CHAR)
			self.layout.addWidget(button, *position)


		# Cancel button
		cancel_button = QPushButton('Cancel')
		cancel_button.setFont(QFont('Arial', 20))
		cancel_button.KEY_CHAR = Qt.Key_Cancel
		self.layout.addWidget(cancel_button, 5, 0, 1, 2)
		cancel_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(cancel_button, cancel_button.KEY_CHAR)
		cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Maj button
		maj_button = QPushButton('MAJ')
		maj_button.setFont(QFont('Arial', 20))
		maj_button.KEY_CHAR = Qt.Key_Shift
		self.layout.addWidget(maj_button, 5, 2, 1, 2)
		maj_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(maj_button, maj_button.KEY_CHAR)
		maj_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Space button
		space_button = QPushButton('Space')
		space_button.setFont(QFont('Arial', 20))
		space_button.KEY_CHAR = Qt.Key_Space
		self.layout.addWidget(space_button, 5, 4, 1, 2)
		space_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
		space_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		# Back button
		back_button = QPushButton('Back')
		back_button.setFont(QFont('Arial', 20))
		back_button.KEY_CHAR = Qt.Key_Backspace
		self.layout.addWidget(back_button, 5, 6, 1, 2)
		back_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
		back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


		# Done button
		done_button = QPushButton('Done')
		done_button.setFont(QFont('Arial', 20))
		done_button.KEY_CHAR = Qt.Key_Home
		self.layout.addWidget(done_button, 5, 8, 1, 2)
		done_button.clicked.connect(self.signalMapper.map)
		self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
		done_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Insert Grid in Vertical Layout
		self.verticalLayout.insertLayout(3,self.layout)
		self.setLayout(self.verticalLayout)


	def convertLetters(self):
		# Check what is the actual keyboard
		if self.maj==True:
			names=self.namesMin
			self.maj=False
		else:
			names = self.namesMaj
			self.maj=True
		# Changes button placeholder and add new mapping
		for i in range(0, len(names)):
			row, col, rowspan, colspan = self.layout.getItemPosition(i)
			self.layout.itemAtPosition(row, col).widget().setText(names[i])
			self.layout.itemAtPosition(row, col).widget().KEY_CHAR = ord(names[i])
			self.signalMapper.setMapping(self.layout.itemAtPosition(row, col).widget(), self.layout.itemAtPosition(row, col).widget().KEY_CHAR)

	def buttonClicked(self, char_ord):

		txt = self.text_box.text()

		if char_ord == Qt.Key_Backspace:
			txt = txt[:-1]
			if len(txt)==0 and not self.maj:
				self.convertLetters()
		elif char_ord == Qt.Key_Home:
			self.parent.setFocus()
			self.parent.ui.nameInput.setText(txt)
			self.hide()
			return
		elif char_ord == Qt.Key_Shift:
			self.convertLetters()
		elif char_ord == Qt.Key_Space:
			txt += ' '
		elif char_ord == Qt.Key_Cancel:
			self.parent.setFocus()
			self.hide()
			return
		else:
			txt += chr(char_ord)
			if len(txt) == 1 and self.maj:
				self.convertLetters()

		self.setFocus()
		self.text_box.setText(txt)
