#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegion
from PyQt5.QtCore import QTime, QTimer, QRect, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from replay import Replay
from module import Module
import modules
from ui.game_ui import Ui_Form as GameWidget

class GameOverChecker():
	def __init__(self, conditionType, limit):
		self.conditionType = conditionType
		self.limit = limit
	
	def check(self, time, scores):
		'''
		Checks if a game is over and return the winner if that's the case
		Either returns -1 if the game is not finished or the highest score's index (0 or 1)
		
		Takes the game time is seconds and a list containing the two scores
		'''
		
		# Gets the index of the highest scoring player (either 0 or 1)
		bestPlayer = scores.index(max(scores))
		
		if self.conditionType=='score' and scores[bestPlayer]>=self.limit:
			return bestPlayer
		elif self.conditionType=='time' and time>self.limit:
			return bestPlayer
		else:
			return -1
		
class GameModule(Module):
	def __init__(self, parent=None):
		super().__init__(parent, GameWidget())

		# Timer managment
		self.timerUpdateChrono = QTimer(self)
		self.timerUpdateChrono.timeout.connect(self.updateChrono)

		# Button connections
		self.ui.btnScore1.clicked.connect(lambda: self.goal(0))
		self.ui.btnScore2.clicked.connect(lambda: self.goal(1))
		
		self.replayer = Replay()
	
	def load(self):
		logging.debug('Loading GameModule')

		self.gameStartTime = QTime.currentTime()
		self.timerUpdateChrono.start(1000)
		self.ui.lcdChrono.display(QTime(0,0).toString("hh:mm:ss"))
		
		self.gameoverChecker = GameOverChecker('score', 10)

		self.scores = [0, 0]
		self.updateScores()

	def unload(self):
		logging.debug('Unloading GameModule')
		del self.gameStartTime
		self.timerUpdateChrono.stop()
	
	def other(self, **kwargs):
		logging.debug('Other GameModule')
	
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
			self.ui_handleClick_btnCancel()
		elif e.key() == Qt.Key_Left:
			self.goal(0)
		elif e.key() == Qt.Key_Right:
			self.goal(1)

	def updateChrono(self):
		# Updated each second
		self.ui.lcdChrono.display(QTime(0,0).addSecs(self.getGameTime()).toString("hh:mm:ss"))
		
		# Don't check scores while showing a replay to avoid closing the engame screen too soon
		if not self.showingReplay:
			self.checkEndGame()

	def getGameTime(self):
		return self.gameStartTime.secsTo(QTime.currentTime())
	
	def updateScores(self):
		self.ui.btnScore1.setText(str(self.scores[0]))
		self.ui.btnScore2.setText(str(self.scores[1]))
		self.checkEndGame()
		
	def goal(self, side):
		if side!=0 and side!=1:
			logging.error('Wrong goal side: {}'.format(side))
		else:
			self.scores[side] += 1
			
			# Show replay
			# May require `sudo apt-get install qtmultimedia5-examples` in order to install the right libraries
			replayFile = self.mainwin.getContent("replay{}.mp4".format(side))
			
			if os.path.exists(replayFile):
				self.showingReplay = True
				
				self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
				self.player.stateChanged.connect(self.endOfReplay)
				self.player.setMuted(True)
				self.player.setVideoOutput(self.ui.videoWidget)
				self.player.setMedia(QMediaContent(QUrl.fromLocalFile(replayFile)))
				self.player.play()
				self.ui.videoWidget.setFullScreen(True)
	
	def endOfReplay(self, status):
		if status!=QMediaPlayer.PlayingState:
			self.ui.videoWidget.setFullScreen(False);
			self.showingReplay = False
			self.updateScores()
			

	def ui_handleClick_btnCancel(self):
		self.switchModule(modules.MenuModule)
		
	def checkEndGame(self):
		win = self.gameoverChecker.check(self.getGameTime(), self.scores)
		
		if win>=0:
			self.send(modules.EndGameModule, winner=win)
			self.switchModule(modules.EndGameModule)
