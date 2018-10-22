#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 18:34:40 2018

@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
"""

import json
import main

class Setting(object):
	TypeName = ''
	
	def __init__(self, value):
		self.value = value

class SettingBoolean(Setting):
	TypeName = 'boolean'
	
	def __init__(self, value):
		Setting.__init__(self, value)

class SettingCombo(Setting):
	TypeName = 'combo'
	
	def __init__(self, value, values):
		Setting.__init__(self, value)
		self.values = values
		
		if self.value not in values:
			raise ValueError('Setting value {} not in list of possible values {}'.format(self.value, self.values))

class SettingRange(Setting):
	TypeName = 'range'
	
	def __init__(self, value, limits):
		Setting.__init__(self, value)
		self.lower_limit = min(limits)
		self.upper_limit = max(limits)
		
		if self.value<self.lower_limit or self.value>self.upper_limit:
			raise ValueError('Setting value {} not in range {}'.format(self.value, (self.lower_limit, self.upper_limit)))
		
class SettingsHolder(object):
	def __init__(self, settingsPath):
		self.settingsPath = settingsPath
		self.loadSettingsFromJSON()
			
	def __delitem__(self, key):
		pass

	def __getitem__(self, key):
		subkeys = SettingsHolder._parseKey(key)
		
		if len(subkeys) == 2:
			return getattr(self, subkeys[0])[subkeys[1]].value
		elif len(subkeys) == 1:
			return getattr(self, subkeys[0]).value
		else:
			raise IndexError('Invalid key {}'.format(key))
	
	def __setitem__(self, key, value):
		subkeys = SettingsHolder._parseKey(key)
		
		if len(subkeys) == 2:
			getattr(self, subkeys[0])[subkeys[1]].value = value
		elif len(subkeys) == 1:
			getattr(self, subkeys[0]).value = value
		else:
			raise IndexError('Invalid key {}'.format(key))
	
	@staticmethod
	def _parseKey(key):
		return [k for k in key.split('.') if k]
		
	def _init_ui(self):
		self.ui.append(Setting())

	def loadSettingsFromJSON(self):
		settings = list()
		
		with open(self.settingsPath, 'r') as f:
			content = json.load(f)
			
			# Outer loop, setting category
			for cat in content:
				setattr(self, cat, dict())
				content_outer = content[cat]
				
				# Inner loop, setting type
				for name in content_outer:
					content_inner = content_outer[name]
					typeName = content_inner['type']
					value = content_inner['value']
					
					# Switch over types
					if typeName == SettingBoolean.TypeName:
						setting = SettingBoolean(value)
					elif typeName == SettingCombo.TypeName:
						setting = SettingCombo(value, content_inner['values'])
					elif typeName == SettingRange.TypeName:
						setting = SettingRange(value, content_inner['range'])
					else:
						raise ValueError('Unknown setting type {}'.format(typeName))

					getattr(self, cat)[name] = setting

Settings = SettingsHolder(main.MainWin.getContent('settings.json'))
