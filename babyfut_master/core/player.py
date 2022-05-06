#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modif : Yoann Malot, Thibaud Le Graverend
"""

import os
import logging
from math import sqrt
from http import HTTPStatus
from datetime import date, timedelta

from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication

from ..babyfut_master import getMainWin, IMG_PATH
from .ginger import Ginger, GingerError
from .database import Database, DatabaseError
from ..ui.consent_dialog_ui import Ui_Dialog as ConsentDialogUI


'''QDialog asking for consent of every new player badging before register in DB'''
class ConsentDialog(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.ui = ConsentDialogUI()
		self.ui.setupUi(self)

		self.ui.txtConsent.setHtml(QCoreApplication.translate('consent', '''<p>
			You are about to connect yourself for the first time. We will need to access:
			<ul>
				<li>Your Name and Surname</li>
				<li>Your Picture (if public)</li>
				<li>...</li>
			</ul>
			</p>

			<p>
			It is possible to play withtout connecting yourself, but this will allow you to keep track of your score and to provide a better experience for you and the ones you play with!
			<br/><br/>
			Do you agree with this? Press ENTER to accept.
			</p>'''))

	def keyPressEvent(self, e):
		if e.key()==Qt.Key_Return:
			self.accept()
		else:
			self.reject()
		

'''
Class handling Player objects. Owns every info of a player and its statistics
Should be constructed with the statics methods fromRFID or loadFromDB.
Guests player are handled with a pointer to a special Player Object, returned by playerGuest() static method.
'''
class Player(QObject):

	_playerGuest = None #Pointer to a unique Guest Player Object

	_default_pic_path = ':ui/img/placeholder_default.jpg'
	_placeholder_pic_path = ':ui/img/placeholder_head.jpg'
	_imgLocalPath         = os.path.join(IMG_PATH, '{}.png')

	def __init__(self, login, fname, lname, stats, elo, private):
		QObject.__init__(self)
		self.login = login
		self.fname = fname
		self.lname = lname
		self.eloRating = elo
		self.private = private

		if self.login=='guest':
			#Set Guest Picture
			self.pic_path = Player._placeholder_pic_path

		elif os.path.isfile(Player._imgLocalPath.format(self.login)):
			#Set Player's personal picture
			self.pic_path = Player._imgLocalPath.format(self.login)
		else:
			#Set default picture for known players
			self.pic_path = Player._default_pic_path

		if stats==None:
			self.stats = self.Stat()
		else:
			self.stats = stats

		# call to method - Delete players that haven't played in a year
		self.deleteOldPlayers()
		

	'''Returns a Player object from a RFID code. 
	Makes a Ginger request, search in DB and creates the Player Object
	Asks for consent and inserts it in DB if new '''
	@staticmethod
	def fromRFID(rfid):
		try:
			infosPlayer = Ginger.instance().getRFID(rfid)
		except GingerError as e:
			logging.warn('Ginger API Error : {}'.format(e))
			return Player.playerGuest()
		
		
		if not Database.instance().loginExists(infosPlayer['login']):					
			# Ask for consent
			consentDialog = ConsentDialog(getMainWin())
			consentDialog.exec()
			if consentDialog.result()==QDialog.Accepted:
				Database.instance().insertPlayer(infosPlayer['login'], infosPlayer['prenom'], infosPlayer['nom'], 1500)
			else:
				logging.info('Consent refused when retrieving a player, returning Guest')
				return Player.playerGuest()

		return Player.loadFromDB(infosPlayer['login'])

	'''Creates and returns a Player object from a login.
		If not found in DB, returns the playerGuest.'''
	@staticmethod
	def loadFromDB(login):
		db = Database.instance()
		try:
			# Retrieve generic informations
			login, fname, lname, elo, private = db.selectPlayer(login)

			# Retrieve stats
			time_played, goals_scored, games_played, victories = db.selectStats(login)
			stats = Player.Stat(time_played, goals_scored, games_played, victories)

			return Player(login, fname, lname, stats, elo, private)

		except DatabaseError as e:
			logging.warn('DB Error: {}'.format(e))
			return Player.playerGuest()


	'''Displays the player's picture in the given widget'''
	def displayImg(self, container_widget):
		self.pic_container=container_widget
		self.pic_container.setStyleSheet('border-image: url({});'.format(self.pic_path))
		QApplication.processEvents()


	def makePrivate(self, option):
		self.private = option
		Database.instance().setPlayerPrivate(self.login, option)

	def deletePlayer(self):
		Database.instance().deletePlayer(self.login)

	def deleteOldPlayers(self):
		today = date.today()
		oneYear = timedelta(weeks=52)
		limitDate = (today-oneYear).strftime("%Y-%d-%m")
		Database.instance().deleteOldPlayers(aYearAgo=limitDate)

	'''Concatenates both names for displaying. To be called like an attribute.'''
	@property
	def name(self):
		return '{} {}'.format(self.fname, self.lname.upper())

	'''Class handling different stats of a player. Acts more like a namespace.'''
	class Stat:
		def __init__(self, time_played=0, goals_scored=0, games_played=0, victories=0):
			self.time_played = time_played if time_played else 0
			self.goals_scored = goals_scored if goals_scored else 0
			self.games_played = games_played if games_played else 0
			self.victories = victories if victories else 0

			#Calculate Index of Perf based on ratio weighted by number of game played
			#Middle of confidence Intervalle on theorical %age of victories
			if self.games_played==0:
				self.ratioIndex =0
			else:
				n = self.games_played
				p = self.victories/n
				u = 1.96 #For confidence rate at 95%
				sup = (2*n*p+u*u+sqrt(u*u+4*n*p*(1-p)))/(2*n+2*u*u)
				inf = (2*n*p+u*u-sqrt(u*u+4*n*p*(1-p)))/(2*n+2*u*u)
				self.ratioIndex=(sup+inf)/2

	'''Returns a list of all players in DB with are not private. Used by Leaderboard.'''
	@staticmethod
	def allStoredPlayers():
		return [Player.loadFromDB(row[0]) for row in Database.instance().selectAllPlayer()]

	'''Returns the instance of the Guest Player object.'''
	@staticmethod
	def playerGuest():
		if not Player._playerGuest:
			Player._playerGuest = Player('guest', 'Guest','', None, 1500, 0)
		return Player._playerGuest
		