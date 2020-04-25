#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QRegion
from PyQt5.QtCore import QDateTime, QDate, QTime, QTimer, QRect, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from .. import modules
from ..core.player import Player
from common.side import Side
from ..core.replay import Replay
from ..core.module import Module
from common.settings import Settings
from ..ui.game_ui import Ui_Form as GameWidget
from ..babyfut_master import getContent

class GameOverChecker():
	def __init__(self, conditionType, limit):
		self.conditionType = conditionType
		self.limit = limit

	def check(self, time, scores):
		'''
		Checks if a game is over and return the winner if that's the case
		Returns the winning side or Side.Undef otherwise

		Takes the game time is seconds and a list containing the two scores
		'''

		# Gets the index of the highest scoring player
		bestPlayer = max(scores, key=scores.get)

		if self.conditionType=='score' and scores[bestPlayer]>=self.limit:
			return bestPlayer
		elif self.conditionType=='time' and time>=self.limit:
			return bestPlayer
		else:
			return Side.Undef

class ReplayHolder(QVideoWidget):
	def __init__(self, mediaPlayer, parent):
		super().__init__(parent)
		self.mediaPlayer = mediaPlayer

	def keyPressEvent(self, e):
		self.mediaPlayer.stop_replay(QMediaPlayer.StoppedState)

class ReplayPlayer(QMediaPlayer):
	def __init__(self, parent):
		super().__init__(parent, QMediaPlayer.VideoSurface)
		self.stateChanged.connect(self.stop_replay)
		self.setMuted(True)

	def start_replay(self, video_file):
		self.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
		self._playerWidget = ReplayHolder(self, self.parent())
		self.setVideoOutput(self._playerWidget)

		self.play()
		self._playerWidget.setFullScreen(True)

	def stop_replay(self, status):
		if status==QMediaPlayer.StoppedState:
			self._playerWidget.setFullScreen(False)
			self._playerWidget.setVisible(False)
			self.parent().endOfReplay()

class GameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, GameWidget())

		# Timer managment
		self.timerUpdateChrono = QTimer(self)
		self.timerUpdateChrono.timeout.connect(self.updateChrono)

		# Button connections
		self.ui.btnScore1.clicked.connect(lambda: self.goal(Side.Left))
		self.ui.btnScore2.clicked.connect(lambda: self.goal(Side.Right))

		
		self.video_player = None #Flag showing if a replay is being played
		self.replayPath = getContent('replay_received.mp4')

	def load(self):
		logging.debug('Loading GameModule')

		self.gameStartTime = QTime.currentTime()
		self.timerUpdateChrono.start(1000)
		self.ui.lcdChrono.display(QTime(0,0).toString("hh:mm:ss"))

		#self.video_player = None
		#if self.camera:
		#	self.camera.start_recording()

		gameover_type = Settings['gameover.type']
		gameover_value = Settings['gameover.value']

		if gameover_type=='time':
			gameover_value *= 60

		self.gameoverChecker = GameOverChecker(gameover_type, gameover_value)

		# if all([len(val)==0 for val in self.players.values()]):
		# 	self.players[Side.Left ].append(PlayerGuest)
		# 	self.players[Side.Right].append(PlayerGuest)

		self.scores = {Side.Left: 0, Side.Right: 0}
		self.updateScores()

	def unload(self):
		logging.debug('Unloading GameModule')

		self.timerUpdateChrono.stop()
		self.gameStartTime = None


	def other(self, **kwargs):
		logging.debug('Other GameModule')

		for key, val in kwargs.items():
			if key=='goal' and 'source' in kwargs:
				self.goal(kwargs['source'])

			elif key=='players':
				self.players = val


	def resizeEvent(self, event):
		# 40% of the window width to have (5% margin)-(40% circle)-(10% middle)-(40% circle)-(5% margin)
		btnDiameter = self.mainwin.width()*0.4
		region = QRegion(QRect(0, 0, btnDiameter, btnDiameter), QRegion.Ellipse)
		self.ui.btnScore1.setMinimumSize(btnDiameter, btnDiameter)
		self.ui.btnScore2.setMinimumSize(btnDiameter, btnDiameter)
		self.ui.btnScore1.setMask(region)
		self.ui.btnScore2.setMask(region)

		QtWidgets.QWidget.resizeEvent(self, event)

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			ret = QMessageBox.question(self, 'Stop the match?', 'Do you really want to stop this match? It wont be saved.')
			if ret == QMessageBox.Yes:
				self.handleCancel()
		
		'''
		Enable scoring goals with Keyboard
		elif e.key() == Qt.Key_Left:
			self.goal(Side.Left)

		elif e.key() == Qt.Key_Right:
			self.goal(Side.Right)
		'''

	def updateChrono(self):
		# Updated each second
		self.ui.lcdChrono.display(QTime(0,0).addSecs(self.getGameTime()).toString("hh:mm:ss"))

		# Don't check scores while showing a replay to avoid closing the engame screen too soon
		if not self.video_player:
			self.checkEndGame()

	def getGameTime(self):
		return self.gameStartTime.secsTo(QTime.currentTime())

	def updateScores(self):
		self.ui.btnScore1.setText(str(self.scores[Side.Left]))
		self.ui.btnScore2.setText(str(self.scores[Side.Right]))
		self.checkEndGame()

	def goal(self, side):
		if side not in Side:
			logging.error('Wrong goal side: {}'.format(side))
		elif not self.video_player:
			self.scores[side] += 1
			print('goal ici')

			if os.path.exists(self.replayPath) and Settings['replay.activated']:
				self.video_player = ReplayPlayer(self)
				self.video_player.start_replay(self.replayPath)
			else:
				#If replay showed, updateScores is called at end OfReplay
				self.updateScores()


	def endOfReplay(self):
		self.video_player = None

		if self.gameStartTime:
			self.updateScores()
		# if self.camera:
		# 	self.camera.start_recording()

	def handleCancel(self):
		self.switchModule(modules.MenuModule)

	def checkEndGame(self):
		winSide = self.gameoverChecker.check(self.getGameTime(), self.scores)

		if winSide!=Side.Undef:
			start_timestamp = int(QDateTime(QDate.currentDate(), self.gameStartTime).toMSecsSinceEpoch()/1000)

			self.send(modules.EndGameModule, players=self.players, winSide=winSide, scores=self.scores)
			self.send(modules.EndGameModule, start_time=start_timestamp, duration=self.getGameTime(), gameType=self)
			self.switchModule(modules.EndGameModule)
