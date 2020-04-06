#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import uuid

from pr_baby_app_esclave.core.player import Side
from pr_baby_app_esclave.core.settings import Settings

class Message:
    def __init__(self):
        self._idMsg = str(uuid.uuid4())

    def getIdMsg(self):
        return self._idMsg


class MessageGoal(Message):
    def __init__(self):
        Message.__init__(self)
        self._type = "goal"
        self.side = Side.Left if Settings['app.side']=='left' else Side.Right
    """ a voir si on peut envoyer le replay en meme temps """
    
    def getMessage(self):
        message = self._idMsg + "\t" + self._type + "\t" #+ self.side
        return message.encode()


class MessageRFID(Message):
    def __init__(self, rfid_code):
        Message.__init__(self)
        self._type = "rfid"
        self.rfidCode = rfid_code

    def getMessage(self):
        message = self._idMsg + "\t" + self._type + "\t" + self.rfidCode
        return message.encode()


class MessageReplay(Message):
    """ voir comment envoyer un fichier video et maybe supp cette classe et tout envoyer avec messageGoal"""
    def __init__(self):
        Message.__init__(self)
        self._type = "replay"
        self.side = "right"

    def getMessage(self):
        message = self._idMsg + "\t" + self._type + "\t" + self.side
        return message.encode()
