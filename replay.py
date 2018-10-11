#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
from settings import Settings

onRasp = os.uname()[1] == 'raspberrypi'

if onRasp:
	import picamera


class Replay():
	def __init__(self):
		if onRasp:
			self.cam = picamera.PiCamera()
			self.cam.resolution = Settings['picam.resolution']
			self.cam.framerate = Settings['picam.fps']
			self.cam.hflip = Settings['picam.hflip']
			self.cam.vflip = Settings['picam.vflip']
			self.format = Settings['picam.format']
			self.continue_recording = False
			self.stream = picamera.PiCameraCircularIO(self.cam, seconds=Settings['replay.duration'])
	
	def capture(self, fileToSave):
		if onRasp:
			self.cam.start_recording(self.stream, self.format)
			self.continue_recording = True
			
			try:
				while self.continue_recording:
					self.cam.wait_recording(1)
			finally:
				self.cam.stop_recording()
				
			self.stream.copy_to(fileToSave)
			self.cam.close()
			self.stream.close()

	def stop():
		self.continue_recording = False
