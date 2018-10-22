#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
import serial
from os.path import isfile as exists
from autopy.key import tap as PressKey, Code as KeyCode
from threading import Thread

from player import Side

class InputThread(Thread):
	keyButtonBindings = [KeyCode.ESCAPE, KeyCode.UP_ARROW, KeyCode.LEFT_ARROW, KeyCode.RIGHT_ARROW, KeyCode.DOWN_ARROW, KeyCode.RETURN]

	def __init__(self, dispatcher, side):
		Thread.__init__(self)
		self.side = side
		self.dispatcher = dispatcher
		self.continueRunning = True
		self.path = '/dev/ttyUSB0' if self.side==Side.Left else '/dev/ttyUSB1'

		if exists(self.path):
			self.arduino = serial.Serial(self.path, 9600, timeout=1)
		else:
			raise RuntimeError('No arduino connected on the {} side'.format(self.side.name.lower()))

	def run(self):
		while self.arduino.isOpen():
			msg = self.arduino.readline()[:-1]

			if msg:
				parsedMessage = self.parseMsg(msg)
				if 'butn' in parsedMessage:
					self.sendKeyStroke(parsedMessage)
				else:
					self.dispatcher.dispatchMessage(parsedMessage)
			else:
				logging.warn('No message read on Arduino {}'.format(self.side.name))

	def stop(self):
		self.continueRunning = False
		self.arduino.close()

	def sendKeyStroke(self, msg):
		if 'butn' in msg:
			button = int(msg['butn'])
			print({button: ['ESCAPE', 'UP_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW', 'DOWN_ARROW', 'RETURN'][button]})
			key = InputThread.keyButtonBindings[button]
			PressKey(key, [])

	def parseMsg(self, msg):
		parts = msg.split(':')
		return {parts[0]: parts[1], 'source': self.side}
