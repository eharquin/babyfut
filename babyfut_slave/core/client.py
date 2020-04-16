#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import socket, pickle, threading
from PyQt5.QtCore import QObject

from common.message import *


host = "localhost"
port = 15555

class Client(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.connect((host, port))
        print("Client connecté")
        


    def sendMessage(self, message):
        data = pickle.dumps(message)
        self.connexion.send(data)


    def sendGoal(self):
        print("Ici")
        self.sendMessage(MessageGoal())

    def sendRFID(self, rfid):
        self.sendMessage(MessageRFID(rfid))

