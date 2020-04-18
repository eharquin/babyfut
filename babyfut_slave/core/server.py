#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.message import Message
import socket, pickle

hote = ''
port = 12800 # TODO put in settings 

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))
socket.listen(5)
client, address = socket.accept()
print(str(client) +"  "+ str(address))

while True:
        response = client.recv(1024)
        if response != "":
                message = pickle.loads(response)
                print(message._type)

socket.close()
client.close()
print("Server closed")
