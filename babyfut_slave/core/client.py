#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import threading, socket, sys, os, time
import pickle


class Message:
    def __init__(self):
        self.idMsg = str(138492)

    def getIdMsg(self):
        return self.idMsg


class MessageGoal(Message):
    def __init__(self):
        Message.__init__(self)
        self.type = "goal"
        self.side = "right"


hote = "localhost"
port = 15555

message = MessageGoal()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

data_to_send = pickle.dumps(message)
socket.send(data_to_send)
print("Closing")
socket.close()
