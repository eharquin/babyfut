#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifications : Yoann MALOT, Thibaud LE GRAVEREND
"""

import logging
import time
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from ..babyfut_master import ON_RASP
from common.side import Side
from common.settings import Settings

if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library
	import pyautogui # PyPi library

class Input(QObject):
	'''
	Defines pins. Uses BCM pin identifiers
	'''
	'''
		_RFIDPins = {
			'pin_rst': 25,
			'pin_ce' :  8,
			'pin_irq': 24
		}

		_GoalPins = {
			'pin_trig':  3,
			'pin_echo':  17
		}
	'''
	_keyButtonBindings = {
		#26: 'up',
		#22: 'left',
		#27: 'right',
		#23: 'down',
		#17: 'return',
		#18: 'escape'

		16: 'up',
		 6: 'left',
		12: 'right',
		13: 'down',
		26: 'return',
		20: 'del',
		19: 'escape'
	}

	def __init__(self):
		QObject.__init__(self)
		self.last_input = time.time()

		if ON_RASP:
			GPIO.setmode(GPIO.BCM)
			for pin in self._keyButtonBindings.keys():
				GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
				GPIO.add_event_detect(pin, GPIO.RISING, callback=self._handleButtonPress)

			self.side = Side.Left if Settings['app.side']=='left' else Side.Right
			

	def _handleButtonPress(self, button_pin):
		arrival_time = time.time()
		if button_pin not in Input._keyButtonBindings.keys():
			logging.warn('Unknown button pin: {}'.format(button_pin))
		elif arrival_time-self.last_input>0.5:
			self.last_input = arrival_time
			key = self._keyButtonBindings[button_pin]
			logging.debug('Sending {} as {}'.format(button_pin, key))
			pyautogui.press(key)
