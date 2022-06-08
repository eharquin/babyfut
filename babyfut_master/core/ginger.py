#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modif : Yoann Malot, Thibaud Le Graverend, Adam Soimansoib
"""
import json
import logging
import requests
from http import HTTPStatus

class GingerError(Exception):
	pass

'''
Singleton class in charge of the communication with the Ginger API. 
'''
class Ginger(object):
	#URL = 'https://assos.utc.fr/ginger/v1/'
	
	#faux-ginger URL, in local
	URL = 'http://localhost/faux-ginger/index.php/v1/'
	_instance = None

	def __init__(self):
		if not Ginger._instance:
			#Real API key to be found in Settings
			#self.api_key = Settings['ginger.key']

			#faux-ginger key
			self.api_key  = 'fauxginger'
			self.url = Ginger.URL

	@staticmethod
	def instance():
		if Ginger._instance==None:
			Ginger._instance = Ginger()
		return Ginger._instance

	'''Returns dictionnary of personal infos from a RFID code'''
	def getRFID(self, rfid):
		# Add the API key to the parameter list
		params= {'key':self.api_key}
		query = self.url+'badge/{}/'.format(rfid)

		# Handle Requests Exception such as ConnectionError. 
		try:
			response = requests.get(query, params)
		except requests.exceptions.RequestException as e:
			raise GingerError("Requests Exception : {}".format(e))

		if response.status_code!=HTTPStatus.OK:
			raise GingerError("HTTP request returned code : {}".format(response.status_code))
		else:
			return json.loads(response.content)
