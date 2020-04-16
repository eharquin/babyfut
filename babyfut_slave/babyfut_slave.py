#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .core.input import Input
from .core.client import Client
def getContent(path):
	contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
	return join(contentFolder, path)

ON_RASP = os.uname()[1] == 'raspberrypi'

if __name__=='__main__':
	__package__ = 'babyfut_slave'
    
    #Starting client communication with master thread
    client = Client()
    client.start()
    
    #Handling RFID and Goal lecture Threads
    input = Input()
   
    #Connecting input's Pyqtsignals to client sending methods 
    input.rfidReceived.connect(lambda rfid: client.sendRFID(rfid))
    input.goalDetected.connect(client.sendGoal)
    input.start()

   

