#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

def getContent(path):
	contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
	return join(contentFolder, path)

ON_RASP = os.uname()[1] == 'raspberrypi'

if __name__=='__main__':
    app = QApplication(sys.argv)
    __package__ = 'babyfut_slave'
    from .core.client import Client
    from .core.input import Input
    
    #Starting client communication with master thread
    client = Client()
    print("coucou bilou")

    #Handling RFID and Goal lecture Threads
    input = Input()

    #Connecting input's Pyqtsignals to client sending methods 
    input.rfidReceived.connect(lambda rfid: client.sendRFID(rfid))
    input.goalDetected.connect(client.sendGoal)
    input.start()

    app.exec_()

   

