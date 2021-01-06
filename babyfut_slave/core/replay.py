#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs: Yoann Malot, Thibaud Le Graverend
"""
import subprocess
from threading import Thread, Event

from ..babyfut_slave import getContent, ON_RASP
from common.settings import Settings
from PyQt5.QtCore import QObject, pyqtSignal


if ON_RASP:
	import picamera

class Replay(Thread,QObject):
	
	readyToSend = pyqtSignal()
	
	def __init__(self):
		Thread.__init__(self)
		QObject.__init__(self)

		self.replayPath = getContent('replay.mp4')
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
			
		print('enregistre1')
	def start_recording(self):
		if self.isCamAvailable():
			print("start")
			self.start_flag.set()

	def stop_recording(self):
		if self.isCamAvailable():
			print("stop")
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
			print("run")
			if not self.shutdown:
				self.cam.start_recording(self.stream, Settings['picam.format'])
				print('enregistre')
				try:
					while not self.stop_flag.is_set():
						self.cam.wait_recording(1)

				finally	:
					print("finaly stop recording")
					self.cam.stop_recording()
				print("copy replay")
				self.stream.copy_to(self.replayPath)
				self.stream.clear()
				self.readyToSend.emit()
                # Set this flag to tell the calling thread that replay is saved
				self.stopped_flag.set()

		self.cam.close()
		self.stream.close()

	@classmethod
	def Dummy(cls):
		return getContent('Replay Right.mp4')

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
