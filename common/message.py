#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import uuid

from common.side import Side
from common.settings import Settings

class Message:
    def __init__(self):
        self.side = 'left' #Side.Left if Settings['app.side']=='left' else Side.Right

    def getSideMsg(self):
        return self.side


class MessageGoal(Message):
    def __init__(self, lenght):
        Message.__init__(self)
        self._type = "goal"
        self.replayLenght = lenght
        #seld._id = 
    

class MessageRFID(Message):
    def __init__(self, rfid_code):
        Message.__init__(self)
        self._type = "rfid"
        self.rfidCode = rfid_code


class MessageReplay(Message):
    def __init__(self):
        Message.__init__(self)
        self._type = "replay"

