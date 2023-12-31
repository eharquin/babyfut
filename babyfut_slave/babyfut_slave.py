#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import os, sys, signal, logging
from os.path import dirname, abspath, join, exists

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QCoreApplication
from common.settings import Settings


def getContent(path):
	contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
	return join(contentFolder, path)

ON_RASP = (os.uname()[1] == 'master') or (os.uname()[1] == 'slave') 


if __name__=='__main__':

    logging.basicConfig(level=logging.DEBUG)

    app = QCoreApplication(sys.argv)
    __package__ = 'babyfut_slave'
    from .core.client import Client
    from .core.input import Input
    from .core.replay import Replay

    
    #Allow to quit with ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

   
    #print("Test")
    #Starting client communication with master thread
    client = Client(Settings['network.host'], int(Settings['network.port']))


#    if Replay.isCamAvailable():
#        threadReplay = Replay()
#        threadReplay.start()
#        threadReplay.readyToSend.connect(client.setReplayReady)
		#myapp.dispatchMessage({'replayThread': threadReplay}, toType=GameModule)


    #Handling RFID and Goal lecture Threads
    input = Input()

    #Connecting input's Pyqtsignals to client sending methods 
    input.rfidReceived.connect(lambda rfid: client.sendRFID(rfid))
    input.goalDetected.connect(client.sendGoal)
    
    input.start()

    app.exec_()

    input.stop()
    input.join()
    logging.debug("Input closed properly")
    client.stop()
    logging.debug("Client closed properly")

    if Replay.isCamAvailable():
        threadReplay.stop()
        threadReplay.join()
   

