#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Enzo Harquin, Tom Besson
"""

import subprocess
from threading import Thread

from ..babyfut_slave import getContent, ON_RASP
from common.settings import Settings
from PyQt5.QtCore import QObject

if ON_RASP:
    import picamera


class Replay(QObject):

    def __init__(self):
        print("Initialization")
        QObject.__init__(self)

        self.replayPath = getContent('replay.mp4')

        print(" init cam thread")
        self.camThread = camThread(self)

        self.cam = picamera.PiCamera()
        self.cam.resolution = Settings['picam.resolution']
        self.cam.framerate = Settings['picam.fps']
        self.cam.hflip = Settings['picam.hflip']
        self.cam.vflip = Settings['picam.vflip']

        print(" init circular buffer")
        # initialize the circular buffer
        # default bit rate 17Mbps
        self.stream = picamera.PiCameraCircularIO(self.cam, seconds=Settings['replay.duration'])
        self.bufferLength = 0
        self.lastBufferLength = 0

    def start(self):
        print("cam thread started")
        self.camThread.start()

    def stop(self):
        self.camThread.stop();
        self.camThread.join()

    def create_replay(self):
        self.lastBufferLength = self.bufferLength
        self.bufferLength = self.stream.size
        print(self.bufferLength)
        self.stream.copy_to(self.replayPath)
        self.stream.clear()

    @classmethod
    def Dummy():
        return getContent('Replay Right.mp4')

    @staticmethod
    def detectCam():
        if ON_RASP:
            camdet = subprocess.check_output(["vcgencmd", "get_camera"])
            return bool(int(chr(camdet[-2])))
        else:
            return False

    @staticmethod
    def isCamAvailable(self=None):
        detected = self.camera_detected if self != None else Replay.detectCam()
        return ON_RASP and detected


class camThread(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.isRunning = True

        self.camera_detected = Replay.detectCam()

    def start(self):
        # start the record
        self.parent.cam.start_recording(self.parent.stream, Settings['picam.format'])

        # call run()
        Thread.start(self)

    def stop(self):
        self.isRunning = False

    def run(self):
        while (self.isRunning):
            self.handleCam()

    def handleCam(self):
        if (not self.parent.stop):
            self.parent.cam.wait_recording(1)



