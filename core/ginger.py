#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import logging
import request
from http import HTTPStatus

class Ginger(object):
	URL = 'https://assos.utc.fr/ginger/v1/'
	_instance = None

	def __init__(self):
		if Ginger._instance!=None:
			self.api_key = Settings['ginger.key']
			self.url = Ginger.URL

	@property
	@staticmethod
	def instance():
		if Ginger._instance==None:
			Ginger._instance = Ginger()
		return Ginger._instance

	@staticmethod
	def get(endpoint, params={}):
		# Add the API key to the parameter list
		params['key'] = Ginger.instance.api_key

		response = request.get(Ginger.instance.url + endpoint, params)
		if response.status_code!=200:
			return HTTPStatus(response.status_code)
		else:
			return response.content
