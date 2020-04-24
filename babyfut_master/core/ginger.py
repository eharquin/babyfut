#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""
import json
import logging
import requests
from http import HTTPStatus

class GingerError(Exception):
	pass

class Ginger(object):
	#URL = 'https://assos.utc.fr/ginger/v1/'
	URL = 'http://localhost/faux-ginger/index.php/v1/'
	_instance = None

	def __init__(self):
		if not Ginger._instance:
			print('coucou')
			#self.api_key = Settings['ginger.key']
			self.api_key  = 'fauxginger'
			self.url = Ginger.URL

	@staticmethod
	def instance():
		if Ginger._instance==None:
			Ginger._instance = Ginger()
		return Ginger._instance

	def getRFID(self, rfid):
		# Add the API key to the parameter list
		params= {'key':self.api_key}
		query = self.url+'badge/{}/'.format(rfid)

		response = requests.get(query, params)
		if response.status_code!=200:
			raise GingerError("HTTP request returned code : {}".format(response.status_code))
		else:
			return json.loads(response.content)

	
# code = '01234567'
# infos = Ginger.instance().getRFID(code)

# print(infos)
# print("c'est bon !")