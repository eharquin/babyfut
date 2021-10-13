#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yoann Malot, Thibaud Le Graverend
"""
from PyQt5.QtCore import Qt, QObject, QSignalMapper
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

'''
Use KeyboardWidget to show a Keyboard in your own Window
Use KeyboardDialog to exec an independant Keyboard Dialog attached to your window

For KeyboardWidget the caller should have a fonction def keyboardResult(self, texte=None):
which is called by Keyboard when it finish, with the text entered by the user, 
or None if the Cancelled button has been pressed.

For KeyboardDialog, use method getResult() to access the text once the Dialog has closed

'''

class KeyboardDialog(QDialog):
	def __init__(self, parent, title, placeholder=None):
		QDialog.__init__(self, parent)
		self.setWindowTitle("")
		self.resize(800, 433)
		self.setStyleSheet("color: rgb(52, 53, 77)")
		self.verticalLayout = QVBoxLayout(self)
		self.widget = KeyboardWidget(self, title, placeholder)
		self.verticalLayout.addWidget(self.widget)
		self.text = placeholder

	def keyboardResult(self,texte=None):
		if texte:
			self.text=texte
		self.done(bool(texte))

	def getResult(self):
		return self.text


class KeyboardWidget(QWidget):
	def __init__(self, parent, title, placeholder=None):
		super(KeyboardWidget, self).__init__(parent)
		self.parent = parent
		self.title= title
		self.placeholder=placeholder
		self.signalMapper = QSignalMapper(self)
		self.signalMapper.mapped[int].connect(self.buttonClicked)
		self.setGeometry(0, 0, parent.width(), parent.height())
		self.initUI()

	def initUI(self):
		self.verticalLayout = QVBoxLayout()
		self.layout = QGridLayout()

		self.title = QLabel(self.title)

		self.title.setFont(QFont('Arial', 25))
		self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter)

		self.setAutoFillBackground(True)
		
		self.text_box = QLineEdit()
		self.text_box.setReadOnly(True)
		self.text_box.setMaxLength(30)
		self.text_box.setFont(QFont('Arial', 20))
		if self.placeholder:
			self.text_box.setText(self.placeholder)

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
			self.hide()
			self.parent.keyboardResult(txt)
			return
		elif char_ord == Qt.Key_Shift:
			self.convertLetters()
		elif char_ord == Qt.Key_Space:
			txt += ' '
		elif char_ord == Qt.Key_Cancel:
			self.parent.setFocus()
			self.hide()
			self.parent.keyboardResult()
		else:
			txt += chr(char_ord)
			if len(txt) == 1 and self.maj:
				self.convertLetters()

		self.setFocus()
		self.text_box.setText(txt)

