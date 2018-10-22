#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
from threading import Event
from multiprocessing import Process, Lock

from main import MainWin
from settings import Settings

onRasp = os.uname()[1] == 'raspberrypi'

if onRasp:
	import picamera


class LockableValue():
	def __init__(self, value):
		self.value = value
		self.mutex = Lock()

class Replay():
	def __init__(self, side):
		self.recording = LockableValue(False)
		self.replayPath = MainWin.getContent('Replay {}.mp4'.format(side.name))
		self.stopped = Event()

		if onRasp:
			self.cam = picamera.PiCamera()
			self.cam.resolution = Settings['picam.resolution']
			self.cam.framerate = Settings['picam.fps']
			self.cam.hflip = Settings['picam.hflip']
			self.cam.vflip = Settings['picam.vflip']
			self.format = Settings['picam.format']
			self.stream = picamera.PiCameraCircularIO(self.cam, seconds=Settings['replay.duration'])

	def start_recording(self):
		if not onRasp:
			self.stopped.set()
		else:
			self.recording.value = True
			self.stopped.clear()
			self.capture_process = Process(target=self.__capture)
			self.capture_process.start()

	def stop_recording(self):
		self.recording.val = True
		self.stopped.wait(timeout=2.0)
		return self.replayPath

	def capture(self, fileToSave):
		if onRasp:
			self.cam.start_recording(self.stream, self.format)

			try:
				recording = self.recording.val

				while recording:
					self.cam.wait_recording(1)
					recording = self.recording.val
			finally:
				self.cam.stop_recording()

			self.stopped.set()
			self.stream.copy_to(self.replayPath)
			self.cam.close()
			self.stream.close()
