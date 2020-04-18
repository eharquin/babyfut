#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import socket, pickle, threading
from PyQt5.QtCore import QObject
import os
from common.message import *
from ..babyfut_slave import getContent
from threading import Event
from .replay import Replay

class Client(QObject):
    def __init__(self, host, port):
        QObject.__init__(self)
        self.replayPath = getContent("replay.mp4")
        self.replayReady = Event()
        self.replayReady.clear()

        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.connect((host, port))
        print("Client connecté")

    def sendMessage(self, message):
        data = pickle.dumps(message)
        self.connexion.send(data)


    def sendGoal(self):
        if Replay.isCamAvailable():
            self.replayReady.wait()

        self.sendMessage(MessageGoal(length))
        envoiReplay=self.connexion.recv(1) 
        if os.path.exists(self.replayPath):
            print("Replay trouve\n")
            length=os.path.getsize(self.replayPath)
        self.sendReplay()


    def sendRFID(self, rfid):
        self.sendMessage(MessageRFID(rfid))

    def setReplayReady(self):
        #Slot of the Replay Thread Signal 
        self.replayReady.set()

    def sendReplay(self):        
        with open(self.replayPath, "rb") as video:
            buffer = video.read()
            self.connexion.sendall(buffer)
