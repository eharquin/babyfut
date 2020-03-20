#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""
import subprocess
from threading import Thread, Event

from Babyfut.babyfut import getContent, ON_RASP
from Babyfut.core.settings import Settings

if ON_RASP:
	import picamera

class Replay(Thread):
	def __init__(self, side):
		Thread.__init__(self)
		self.replayPath = getContent('Replay {}.mp4'.format(side.name))
		self.shutdown = False

		if ON_RASP:
			self.camera_detected = Replay.detectCam()

		self.start_flag = Event()
		self.stop_flag = Event()
		self.stopped_flag = Event()

		if self.isCamAvailable():
			self.cam = picamera.PiCamera()
			self.cam.resolution = Settings['picam.resolution']
			self.cam.framerate = Settings['picam.fps']
			self.cam.hflip = Settings['picam.hflip']
			self.cam.vflip = Settings['picam.vflip']
			self.stream = picamera.PiCameraCircularIO(self.cam, seconds=Settings['replay.duration'])

	def start_recording(self):
		if self.isCamAvailable():
			self.start_flag.set()

	def stop_recording(self):
		if self.isCamAvailable():
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

                # Set this flag to tell the calling thread that replay is saved
				self.stopped_flag.set()

		self.cam.close()
		self.stream.close()

	@classmethod
	def Dummy(cls):
		return getContent('Replay Left.mp4')

	@staticmethod
	def detectCam():
		if ON_RASP:
			camdet = subprocess.check_output(["vcgencmd","get_camera"])
			return bool(int(chr(camdet[-2])))
		else:
			return False

	@staticmethod
	def isCamAvailable(self=None):
		detected = self.camera_detected if self!=None else Replay.detectCam()
		return ON_RASP and detected
