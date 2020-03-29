#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import threading, socket

from PyQt5.QtCore import QObject, pyqtSignal
from babyfut_server.babyfut_server import ON_RASP
from babyfut_server.core.player import Side, opposite
from babyfut_server.core.settings import Settings

if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library
	import pyautogui # PyPi library


hote = ''
port = 12800

class Server(threading.Thread, QObject):

    goalDetected = pyqtSignal(Side)

    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((hote, port))
        self.connexion.listen()
        if ON_RASP:
            self.side = Side.Left if Settings['app.side']=='left' else Side.Right
            self.side = opposite(self.side)
        print("Waiting for connection with client\n")

    def bytetoArray(self, bite):
    	res=0
    	for i in range(4):
    		res += bite[i]<<(i*8)
    	return res

    def run(self):
        while 1:
            self.connexion_client, self.infos_connexion = self.connexion.accept()
            print("Connection established with client\n")
            msg_receive = self.connexion_client.recv(4)
            currentsize=0
            print("reception taille replay")
            sizetoHave = self.bytetoArray(msg_receive)
            print("\tsizeToHave ", sizetoHave);
            with open('./content/Replay Right.mp4', "wb") as video:
                print("reception du replay")
                while sizetoHave > currentsize:
                    buffer = self.connexion_client.recv(1024)
                    if not buffer :
                        break
                    if len(buffer) + currentsize >= sizetoHave:
                        #print("len buffer ", len(buffer))
                        video.write(buffer)
                        currentsize += len(buffer)
                        print(currentsize)
                    else:
                        video.write(buffer)
                        #print(currentsize)
                        currentsize += 1024
                print("fin de reception..")
                if ON_RASP:
                    self.goalDetected.emit(self.side)
                    print("envoie signal OK")
            self.connexion_client.close()
        self.__close__()

    def closeConn(self):
        self.connexion_client.send("FIN".encode())
        self.__close__()

    def stop(self):
        self._running = False

    def __close__(self):
        print("Connection stoped\n")
        self.connexion.close()
