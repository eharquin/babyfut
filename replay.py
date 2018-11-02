#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

from threading import Thread, Event

from main import MainWin, OnRasp
from settings import Settings

if OnRasp:
	import picamera

class Replay(Thread):
	def __init__(self, side):
		Thread.__init__(self)
		self.replayPath = MainWin.getContent('Replay {}.mp4'.format(side.name))
		self.shutdown = False
		
		self.start_flag = Event()
		self.stop_flag = Event()
		self.stopped_flag = Event()

		if OnRasp:
			self.cam = picamera.PiCamera()
			self.cam.resolution = Settings['picam.resolution']
			self.cam.framerate = Settings['picam.fps']
			self.cam.hflip = Settings['picam.hflip']
			self.cam.vflip = Settings['picam.vflip']
			self.stream = picamera.PiCameraCircularIO(self.cam, seconds=Settings['replay.duration'])

	def start_recording(self):
		if OnRasp:
			self.start_flag.set()
			
	def stop_recording(self):
		if OnRasp:
			self.stop_flag.set()
			self.stopped_flag.wait()
			
            # Clear all control flags
			self.stop_flag.clear()
			self.start_flag.clear()
			self.stopped_flag.clear()

		return self.replayPath

	def stop(self):
		self.start_flag.set()
		self.shutdown = True
	
	def run(self):
		while not self.shutdown:
			self.start_flag.wait()
		
			if not self.shutdown:
				self.cam.start_recording(self.stream, Settings['picam.format'])
				try:
					while not self.stop_flag.is_set():
						self.cam.wait_recording(1)
				
				finally	:
					self.cam.stop_recording()
    
				self.stream.copy_to(self.replayPath)
				self.stream.clear()

                # Set this flag to tell the calling thread that replay is saved
				self.stopped_flag.set()

		self.cam.close()
		self.stream.close()
	
	@staticmethod
	def isCamAvailable():
		return OnRasp # and other checks (ToDo)
