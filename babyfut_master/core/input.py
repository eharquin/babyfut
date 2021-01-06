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

'''
Class in charge of the joystick and buttons. Gets GPIO signals and simulates Keyboard pressing.
'''
class Input(QObject):
	
	
	'''Binds pins with corresponding keyboard key. Uses BCM pin identifiers'''
	_keyButtonBindings = {
		15: 'escape',
		14: 'del',
		17: 'right',
		18: 'return',
		22: 'down',
		23: 'up',
		27: 'left'
		
	}

	'''Connects every input pin to  _handleButtonPress method'''
	def __init__(self):
		QObject.__init__(self)
		self.last_input = time.time()

		if ON_RASP:
			GPIO.setmode(GPIO.BCM)
			for pin in self._keyButtonBindings.keys():
				GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
				GPIO.add_event_detect(pin, GPIO.RISING, callback=self._handleButtonPress)

			self.side = Side.Left if Settings['app.side']=='left' else Side.Right
			

	'''Called when input signel is received on Raspberry. Simulates binding key pressing.
		Checks that only one key pressing is done during all the time of input.
	'''
	def _handleButtonPress(self, button_pin):
		arrival_time = time.time()
		print("Button pressed : {}".format(button_pin));
		if button_pin not in Input._keyButtonBindings.keys():
			logging.warn('Unknown button pin: {}'.format(button_pin))
		elif arrival_time-self.last_input>0.5:
			self.last_input = arrival_time
			key = self._keyButtonBindings[button_pin]
			logging.debug('Sending {} as {}'.format(button_pin, key))
			pyautogui.press(key)
