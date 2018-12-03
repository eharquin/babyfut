#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
import pyautogui # PyPi library
from threading import Thread

from babyfut import OnRasp

if OnRasp:
	import RPi.GPIO as GPIO

from player import Side

class GPIOThread(Thread):
	_keyButtonBindings = {
		26: 'up',
		22: 'left',
		27: 'right',
		23: 'down',
		17: 'return',
		18: 'escape'
	}

	def __init__(self, dispatcher):
		Thread.__init__(self)
		self.dispatcher = dispatcher
		self.continueRunning = True
		
		if OnRasp:
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BCM)

			for pin in GPIOThread._keyButtonBindings.keys():
				print(pin)
				GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
				GPIO.add_event_detect(pin, GPIO.RISING, callback=self.handleButtonPress)

	def run(self):
		if OnRasp:
			try:
				while self.continueRunning:
					pass
			finally:
				GPIOThread.clean()

	def handleButtonPress(self, button_pin):
		if button_pin not in GPIOThread._keyButtonBindings.keys():
			logging.warn('Unknown button pin: {}'.format(button_pin))
		else:
			key = GPIOThread._keyButtonBindings[button_pin]
			logging.debug('Sending {} as {}'.format(button_pin, key))
			pyautogui.press(key)
	
	def stop(self):
		self.continueRunning = False
	
	@staticmethod
	def clean():
		if OnRasp:
			GPIO.cleanup()
