#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""


import picamera
import time
import threading
import io
import random
import picamera


camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=5)
camera.start_recording('video.h264')
time.sleep(10)
camera.stop_recording()