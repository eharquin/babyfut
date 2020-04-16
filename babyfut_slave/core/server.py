#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#from common.message import *
import socket, pickle

class Message:
    def __init__(self):
        self.side = Side.Left if Settings['app.side']=='left' else Side.Right

    def getSideMsg(self):
        return self.side


class MessageGoal(Message):
    def __init__(self):
        Message.__init__(self)
        self._type = "goal"
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

hote = ''
port = 12800

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))
socket.listen(5)

while True:
        
        client, address = socket.accept()
        response = client.recv(1024)
        if response != "":
                message = pickle.loads(response)
                print(message.type)

socket.close()
print("Server closed")
