#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging

from http import HTTPStatus

from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication

from ..babyfut_master import getMainWin, IMG_PATH
from .downloader import Downloader
from .ginger import Ginger, GingerError
from .database import Database, DatabaseError
from ..ui.consent_dialog_ui import Ui_Dialog as ConsentDialogUI


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

class Player(QObject):

	_playerGuest = None #Pointer to a unique Guest Player Object

	_default_pic_path = ':ui/img/placeholder_default.jpg'
	_placeholder_pic_path = ':ui/img/placeholder_head.jpg'
	_imgLocalPath         = os.path.join(IMG_PATH, '{}.jpg')
	_utcPictureURL        = 'https://demeter.utc.fr/portal/pls/portal30/portal30.get_photo_utilisateur?username={}'

	def __init__(self, login, fname, lname, stats=None):
		QObject.__init__(self)
		self.login = login
		self.fname = fname
		self.lname = lname

		if self.login=='guest':
			#Set Guest Picture
			self.pic_path = Player._placeholder_pic_path

		elif os.path.isfile(Player._imgLocalPath.format(self.login)):
			#Set Player's personal picture
			self.pic_path = Player._imgLocalPath.format(self.login)
		# elif self.login:
			#Set URL to downloda Player's picture
		# 	self.pic_path = Player._utcPictureURL.format(self.login)
		else:
			#Set default picture for known players
			self.pic_path = Player._default_pic_path

		if stats==None:
			self.stats = self.Stat()
		else:
			self.stats = stats

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
				Database.instance().insertPlayer(infosPlayer['login'], infosPlayer['prenom'], infosPlayer['nom'])
			else:
				logging.info('Consent refused when retrieving a player, returning Guest')
				return Player.playerGuest()

		return Player._loadFromDB(infosPlayer['login'])

	@staticmethod
	def _loadFromDB(login):
		db = Database.instance()
		try:
			# Retrieve generic informations
			login, fname, lname = db.selectPlayer(login)

			# Retrieve stats
			# stats = {}
			# stats['time_played'], stats['goals_scored'], stats['games_played'], stats['victories']= db.selectStats(login)

			stats = Player.Stat()
			stats.time_played, stats.goals_scored, stats.games_played, stats.victories = db.selectStats(login)

			# for key, val in stats.items():
			# 	if val==None:
			# 		stats[key] = 0

			return Player(login, fname, lname, stats)

		except DatabaseError as e:
			logging.warn('DB Error: {}'.format(e))
			return PlayerGuest

	@staticmethod
	def _loadFromAPI(rfid):
		'''
		Retrieves a player's informations from the Ginger API
		'''
		try:
			infosPlayer = Ginger.instance().getRFID(rfid)
			Database.instance().insertPlayer(rfid, infosPlayer['nom'], infosPlayer['prenom'])
		except GingerError as e:
			logging.warn('Ginger API Error : {}'.format(e))
			return PlayerGuest

		return Player._loadFromDB(rfid)

	# def displayImg(self, container_widget):
	# 	self.pic_container = container_widget

	# 	if self.pic_path.startswith('http'):
	# 		# Download from the internet but display a temporary image between
	# 		self.pic_container.setStyleSheet('border-image: url({});'.format(Player._placeholder_pic_path))
	# 		Downloader.instance().request(self.pic_path, os.path.join(IMG_PATH, '{}.jpg'.format(self.id)))
	# 		Downloader.instance().finished.connect(self._downloader_callback)
	# 	else:
	# 		# Already downloaded and stored locally
	# 		self.pic_container.setStyleSheet('border-image: url({});'.format(self.pic_path))
	# 		QApplication.processEvents()
	def displayImg(self, container_widget):
		self.pic_container=container_widget
		self.pic_container.setStyleSheet('border-image: url({});'.format(self.pic_path))
		QApplication.processEvents()
		
	# @pyqtSlot(str)
	# def _downloader_callback(self, path):
	# 	# Take the callback if not already done and we are the targer
	# 	if IMG_PATH in path and str(self.id) in path and IMG_PATH not in self.pic_path:
	# 		self.pic_path = path
	# 		Downloader.instance().finished.disconnect(self._downloader_callback)

	# 		if self.pic_container!=None:
	# 			self.displayImg(self.pic_container)

	def forgetPicture(self):
		self.pic_path = Player._placeholder_pic_path
		Database.instance().delete_playerpic(self.login)

	def make_private(self):
		self.private = True
		Database.instance().make_player_private(self.login)

	@property
	def name(self):
		return '{} {}'.format(self.fname, self.lname.upper())

	# @property
	# def stats_property(self):
	# 	'''
	# 	Compatibility property allowing to access stats as a object member and not dict
	# 	ex: player.stats['victories'] can be accessed with player.stats_property.victories'
	# 	This is mostly used for sorting players in leaderboard.py
	# 	'''
	# 	class Stat:
	# 		def __init__(self, stats):
	# 			self.victories = stats['victories']
	# 			self.time_played = stats['time_played']
	# 			self.goals_scored = stats['goals_scored']
	# 			self.games_played = stats['games_played']

	# 	return Stat(self.stats)

	class Stat:
		def __init__(self):
			self.victories = 0
			self.time_played = 0
			self.goals_scored = 0
			self.games_played = 0



	@staticmethod
	def allStoredPlayers():
		return [Player._loadFromDB(row[0]) for row in Database.instance().selectAllPlayer()]

	@staticmethod
	def playerGuest():
		if not Player._playerGuest:
			Player._playerGuest = Player('guest', 'Guest','')
		return Player._playerGuest
		
# PlayerGuest = Player.fromRFID(-1)
PlayerEmpty = Player('', '', Player._placeholder_pic_path, {'time_played':'', 'goals_scored':'', 'games_played':'', 'victories': ''})
