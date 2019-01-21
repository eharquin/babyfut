#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging
from enum import Enum
from http import HTTPStatus

from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSlot, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication

from Babyfut.babyfut import getMainWin, IMG_PATH
from Babyfut.core.downloader import Downloader
from Babyfut.core.ginger import Ginger
from Babyfut.core.database import Database, DatabaseError
from Babyfut.ui.consent_dialog_ui import Ui_Dialog as ConsentDialogUI

class Side(Enum):
	'''
	Values of the enum are used throughout the code for indexing purposes, not to be changed
	'''
	Undef = -1
	Left  = 0
	Right = 1

	@property
	def opposite(self):
		return Side.Right if self==Side.Left else Side.Left

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
			It is possible to play withtout connecting yourslef, but this will allow you to keep track of your score and to provide a better experience for you and the ones you play with!
			<br/><br/>
			Do you agree with this?
			</p>'''))

	def keyPressEvent(self, e):
		if e.key()==Qt.Key_Return:
			self.accept()
		else:
			self.reject()

class Player(QObject):
	__query_infos = 'SELECT id, login, fname, lname FROM Players WHERE rfid==?'
	__query_time_goals_games = 'SELECT SUM(Matchs.duration) AS timePlayed, SUM(Teams.nGoals) AS goalsScored, COUNT(*) AS gamesPlayed FROM Teams INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam OR Teams.id==Matchs.losingTeam) WHERE (Teams.player1==? OR player2==?)'
	__query_victories = 'SELECT COUNT(*) AS victories FROM Players INNER JOIN Teams ON (Players.id==Teams.player1 OR Players.id==Teams.player2) INNER JOIN  Matchs ON (Teams.id==Matchs.winningTeam) WHERE Players.id==?'

	_placeholder_pic_path = ':ui/img/placeholder_head.jpg'
	_imgLocalPath         = os.path.join(IMG_PATH, '{}.jpg')
	_utcPictureURL        = 'https://demeter.utc.fr/portal/pls/portal30/portal30.get_photo_utilisateur?username={}'

	def __init__(self, id, rfid, login, fname, lname, stats=None):
		QObject.__init__(self)
		self.id = id
		self.rfid = rfid
		self.login = login
		self.fname = fname
		self.lname = lname

		if os.path.isfile(Player._imgLocalPath.format(self.id)):
			self.pic_path = Player._imgLocalPath.format(self.id)
		elif self.login:
			self.pic_path = Player._utcPictureURL.format(self.login)
		else:
			self.pic_path = Player._placeholder_pic_path
		
		if stats==None:
			self.stats = { 'time_played': 0, 'goals_scored': 0, 'games_played': 0, 'victories': 0 }
		else:
			self.stats = stats

	@staticmethod
	def fromRFID(rfid):
		if Database.instance().rfid_exists(rfid):
			player = Player._loadFromDB(rfid)
		else:
			### Retrieve player from API
			# Ask for consent
			consentDialog = ConsentDialog(getMainWin())
			consentDialog.exec()

			if consentDialog.result()==QDialog.Accepted:
				player = Player._loadFromAPI(rfid)
			else:
				logging.info('Consent refused when retrieving a player, returning Guest')
				player = PlayerGuest

		return player

	@staticmethod
	def _loadFromDB(rfid):
		db = Database.instance()
		try:
			# Retrieve generic informations
			id, login, fname, lname = db.select_one(Player.__query_infos, rfid)

			# Retrieve stats
			stats = {}
			stats['time_played'], stats['goals_scored'], stats['games_played'] = db.select_one(Player.__query_time_goals_games, id, id)
			stats['victories'], = db.select_one(Player.__query_victories, id)

			for key, val in stats.items():
				if val==None:
					stats[key] = 0

			return Player(id, rfid, login, fname, lname, stats)

		except DatabaseError as e:
			logging.warn('DB Error: {}'.format(e))
			return PlayerGuest

	@staticmethod
	def _loadFromAPI(rfid):
		'''
		Retrieves a player's informations from the Ginger API
		'''
		response = Ginger.instance.get('badge/{}'.format(rfid))
		if isinstance(response, HTTPStatus):
			logging.warn('Request to Ginger failed ({}): returning Guest'.format(response.value))
			return PlayerGuest
		else:
			infos = json.loads(response)
			Database.instance().insert_player(infos['rfid'], infos['login'], infos['nom'], infos['prenom'])

		return Player._loadFromDB(rfid)

	def displayImg(self, container_widget):
		self.pic_container = container_widget

		if self.pic_path.startswith('http'):
			# Download from the internet but display a temporary image between
			self.pic_container.setStyleSheet('border-image: url({});'.format(Player._placeholder_pic_path))
			Downloader.instance().request(self.pic_path, os.path.join(IMG_PATH, '{}.jpg'.format(self.id)))
			Downloader.instance().finished.connect(self._downloader_callback)
		else:
			# Already downloaded and stored locally
			self.pic_container.setStyleSheet('border-image: url({});'.format(self.pic_path))
			QApplication.processEvents()

	@pyqtSlot(str)
	def _downloader_callback(self, path):
		# Take the callback if not already done and we are the targer
		if IMG_PATH in path and str(self.id) in path and IMG_PATH not in self.pic_path:
			self.pic_path = path
			Downloader.instance().finished.disconnect(self._downloader_callback)

			if self.pic_container!=None:
				self.displayImg(self.pic_container)

	def forgetPicture(self):
		self.pic_path = Player._placeholder_pic_path
		self.login = None
		Database.instance().delete_playerpic(self.id)

	def make_private(self):
		self.private = True
		Database.instance().make_player_private(self.id)

	@property
	def name(self):
		return '{} {}'.format(self.fname, self.lname.upper())

	@property
	def stats_property(self):
		'''
		Compatibility property allowing to access stats as a object member and not dict
		ex: player.stats['victories'] can be accessed with player.stats_property.victories'
		This is mostly used for sorting players in leaderboard.py
		'''
		class Stat:
			def __init__(self, stats):
				self.victories = stats['victories']
				self.time_played = stats['time_played']
				self.goals_scored = stats['goals_scored']
				self.games_played = stats['games_played']

		return Stat(self.stats)

	@staticmethod
	def allStoredPlayers():
		return [Player.fromRFID(rfid) for rfid, in Database.instance().select_all_rfid()]

PlayerGuest = Player.fromRFID(-1)
PlayerEmpty = Player(-1, -42, '', '', Player._placeholder_pic_path, {'time_played':'', 'goals_scored':'', 'games_played':'', 'victories': ''})
