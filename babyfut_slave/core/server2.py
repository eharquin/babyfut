#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.message import Message
import socket, pickle

hote = ''
port = 12800

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 23456))

while True:
        socket.listen(5)

        client, address = socket.accept()
        response = client.recv(1024)
        if response != "":
                message = pickle.loads(response)
                print(message._type)

socket.close()
print("Server closed")
