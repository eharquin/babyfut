#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
import time
from threading import Thread
import pyautogui # PyPi library

from PyQt5.QtCore import QObject, pyqtSignal

from Babyfut.babyfut import ON_RASP
from Babyfut.core.player import Side

if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library

class GPIOThread(Thread, QObject):
	_keyButtonBindings = {
		26: 'up',
		22: 'left',
		27: 'right',
		23: 'down',
		17: 'return',
		18: 'escape'
	}

	rfidReceived = pyqtSignal(str)

	def __init__(self):
		Thread.__init__(self)
		QObject.__init__(self)
		self.continueRunning = True
		self.lastRFIDReception = 0

		if ON_RASP:
			self.rf_reader = RFID(pin_rst=25, pin_ce=8, pin_irq=24, pin_mode=GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BCM)

			for pin in GPIOThread._keyButtonBindings.keys():
				print(pin)
				GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
				GPIO.add_event_detect(pin, GPIO.RISING, callback=self.handleButtonPress)

	def run(self):
		if ON_RASP:
			try:
				while self.continueRunning:
					self.rf_reader.wait_for_tag()
					(error, tag_type) = self.rf_reader.request()
					if not error:
						self.handleRFID()
			finally:
				self.clean()

	def handleRFID(self):
		(error, id) = self.rf_reader.anticoll()
		if not error:
			# Prevent RFID "spam" (one second removal delay)
			now = time.time()
			if self.lastRFIDReception!=0 and abs(self.lastRFIDReception-now)>1:
				self.lastRFIDReception = 0
				receivedRFID = ':'.join([str(x) for x in id])
				self.rfidReceived.emit(receivedRFID)
				logging.debug('Received RFID: {}'.format(receivedRFID))
			else:
				self.lastRFIDReception = now

	def handleButtonPress(self, button_pin):
		if button_pin not in GPIOThread._keyButtonBindings.keys():
			logging.warn('Unknown button pin: {}'.format(button_pin))
		else:
			key = GPIOThread._keyButtonBindings[button_pin]
			logging.debug('Sending {} as {}'.format(button_pin, key))
			pyautogui.press(key)

	def stop(self):
		self.continueRunning = False
		# Falsely trigger the rfid reader to stop it waiting
		if ON_RASP:
			self.rf_reader.irq.set()

	def clean(self):
		GPIOThread.clean()
		self.rf_reader.cleanup()

	@staticmethod
	def clean():
		if ON_RASP:
			GPIO.cleanup()
