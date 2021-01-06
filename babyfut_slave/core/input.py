#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs: Yoann Malot, Thibaud Le Graverend
"""

import logging
import time
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from ..babyfut_slave import ON_RASP
from common.side import Side
from common.settings import Settings

if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library
	print("On RASP")

class Input(QObject):
	'''
	Defines pins. Uses BCM pin identifiers
	'''

	_RFIDPins = {
		'pin_rst': 25,
		'pin_ce' :  8,
		'pin_irq': 24
	}

	_GoalPins = {
		'pin_trig':  3,
		'pin_echo':  4,
	}

	#Defining Qt Signals
	rfidReceived = pyqtSignal(str)
	goalDetected = pyqtSignal()


	def __init__(self):
		QObject.__init__(self)
		self.last_input = time.time()

		if ON_RASP:
			GPIO.setmode(GPIO.BCM)

			self.side = Side.Left if Settings['app.side']=='left' else Side.Right
			print(self.side)
			self.rfidThread = RFIDThread(self, **Input._RFIDPins)
			self.goalThread = GoalThread(self, **Input._GoalPins)
		
		else:
			#On Computer, thread detecting goals with keyborad
			self.inputSimulation= InputSimulation(self)

	def start(self):
		if ON_RASP:
			print("input started")
			self.rfidThread.start()
			self.goalThread.start()
		else:
			self.inputSimulation.start()

	def stop(self):
		if ON_RASP:
			self.rfidThread.stop(); self.rfidThread.join()
			self.goalThread.stop(); self.goalThread.join()
		else:
			self.inputSimulation.stop(); self.goalSimulation.join()


class GPIOThread(Thread):
	CLEANED = False

	def __init__(self):
		Thread.__init__(self)
		self._running = True

	def running(self):
		return self._running

	def start(self):
		Thread.start(self)

	def stop(self):
		self._running = False

	def clean(self):
		GPIO.cleanup()

class RFIDThread(GPIOThread):
	def __init__(self, parent, **pins):
		GPIOThread.__init__(self)
		self.parent = parent
		self.lastRFIDReception = 0
		self.rf_reader = RFID(**pins, pin_mode=GPIO.BCM)
		print(self.rf_reader.pin_rst, self.rf_reader.pin_ce, self.rf_reader.pin_irq)

	def run(self):
		try:
			while self.running():
			
				self.rf_reader.wait_for_tag()
				(error, tag_type) = self.rf_reader.request()
				if not error:
					self._handleRFID()
				
		finally:
			self.clean()

	def _handleRFID(self):
		(error, id) = self.rf_reader.anticoll()
		if not error:
			# Prevent RFID "spam" (one second removal delay)
			now = time.time()
			if self.lastRFIDReception!=0 and abs(self.lastRFIDReception-now)>1:
				self.lastRFIDReception = 0
				receivedRFID = ':'.join([str(x) for x in id])
				#self.input.emit(self.parent.side, receivedRFID)
				self.parent.rfidReceived.emit(receivedRFID)
				logging.info('Received RFID: {}'.format(receivedRFID))
			else:
				self.lastRFIDReception = now

	def stop(self):
		GPIOThread.stop(self)

		# Falsely trigger the rfid reader to stop it from waiting
		self.rf_reader.irq.set()

	def clean(self):
		GPIOThread.clean(self)
		self.rf_reader.cleanup()

class GoalThread(GPIOThread):
	def __init__(self, parent, pin_trig, pin_echo):
		GPIOThread.__init__(self)
		self.parent = parent
		self.pin_echo = pin_echo
		self.state = 1

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin_echo, GPIO.IN)


	def run(self):
		try:
			print("Goal thread")

			while self.running():
				if GPIO.input(self.pin_echo) == 1:
					self.state = 1

				if GPIO.input(self.pin_echo) == 0 and self.state == 1:
					self.state = 0
					print("Goal!")
					self.parent.goalDetected.emit()
		finally:
			self.clean()

#Testing Thread started only on computer
class InputSimulation(GPIOThread):
	def __init__(self, parent):
		GPIOThread.__init__(self)
		self.parent = parent
		self.last_goal = time.time()

	def run(self):
		while self.running():
			carac=input("Tapez a pour simuler un goal ou chaine carac pour rfid :")
			if carac=="a":
				self.parent.goalDetected.emit()
			else:
				self.parent.rfidReceived.emit(carac)


	def clean(self):()

