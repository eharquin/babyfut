#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import os
import logging
import urllib.request
from time import sleep
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Downloader(Thread, QObject):
	'''
	Helper for downloading images using queues
	'''

	N_ATTEMPS = 5
	__instance = None
	finished = pyqtSignal(str)

	def __init__(self):
		Thread.__init__(self)
		QObject.__init__(self)

		# Mandatory header if we want servers to accept the request
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib.request.install_opener(opener)

		self._close = False
		self._request_stack = []

	@staticmethod
	def instance():
		if Downloader.__instance==None:
			Downloader.__instance = Downloader()

		return Downloader.__instance

	def request(self, url_in, uri_out, nAttemps=None):
		if nAttemps==None:
			nAttemps = Downloader.N_ATTEMPS

		print('Adding "{}". {} before it'.format(url_in, len(self._request_stack)))

		self._request_stack.append((url_in, uri_out, nAttemps))

	def run(self):
		while not self._close:
			if len(self._request_stack)>0:
				url_in, uri_out, nAttemps = self._request_stack.pop()
				nAttemps -= 1

				urllib.request.urlretrieve(url_in, uri_out)#FIXME , timeout=1000)
				if os.path.exists(uri_out):
					logging.debug('Downloaded "{}". {} still queued'.format(url_in, len(self._request_stack)))
					self.finished.emit(uri_out)
				elif nAttemps!=0:
					logging.info('Failed to download "{}". {} attemps remaining'.format(url_in, nAttemps))
					self.request(url_in, uri_out, nAttemps)

			sleep(1)

	def stop(self):
		self._close = True
