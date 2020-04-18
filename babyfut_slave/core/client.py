#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import socket, pickle, threading
from PyQt5.QtCore import QObject

from common.message import *


class Client(QObject):
    def __init__(self, host, mainPort, replayPort):
        QObject.__init__(self)
        self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mainSocket.connect((host, mainPort))
        print("Client connecté")
        self.replaySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.replaySocket.connect((host, replayPort))


    def sendMessage(self, message):
        data = pickle.dumps(message)
        self.connexion.send(data)

    def sendGoal(self):
        self.sendMessage(MessageGoal())

    def sendRFID(self, rfid):
        self.sendMessage(MessageRFID(rfid))

