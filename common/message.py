#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Thibaud Le Graverend, Yoann Malot
"""

from common.side import Side
from common.settings import Settings

'''Common class used for serialisation of messages between server and client. 
Base Class herited by different types of messages '''
class Message:
    def __init__(self):
        self.side = Side.Left if Settings['app.side']=='left' else Side.Right

    def getSide(self):
        return self.side


class MessageGoal(Message):
    def __init__(self, length):
        Message.__init__(self)
        self.type = "goal"
        self.replayLength = length
        #seld._id = 
    

class MessageRFID(Message):
    def __init__(self, rfid_code):
        Message.__init__(self)
        self.type = "rfid"
        self.rfidCode = rfid_code

    def getRFID(self):
        return self.rfidCode


class MessageKeepAlive(Message):
    def __init__(self):
        Message.__init__(self)
        self.type = 'keepalive'


