#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import socket, pickle, time, select

from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
from ..babyfut_master import ON_RASP, getContent, getMainWin
from common.side import Side
from common.settings import Settings
from common.message import *
from PyQt5.QtWidgets import QMessageBox
if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library
	import pyautogui # PyPi library


class Server(QObject):

    # Signals for goal and rfid detection
    goalSignal = pyqtSignal(Side)
    rfidSignal = pyqtSignal(Side, str)
    clientLostSignal = pyqtSignal(str, str)

    def __init__(self):
        QObject.__init__(self)
        #threading.Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connexion.bind((Settings['network.host'], int(Settings['network.port'])))

        # Wait for connection with 1st slave
        self.connexion.listen(5)
        self.conn_client1, self.info_client1 = self.connexion.accept()
        print("Connexion établi avec client1 " + str(self.conn_client1))

        self.slave1 = ClientThread(self, self.conn_client1, self.info_client1)
        self.slave1.start()
        
        # Wait for 2nd slave
        self.connexion.listen(5)
        self.conn_client2, self.info_client2 = self.connexion.accept()
        print("Connexion établi avec client2 " + str(self.conn_client2))
        
        self.slave2 = ClientThread(self, self.conn_client2, self.info_client2)
        self.slave2.start()


    def stop(self):
        # Stop slave's thread
        self.slave1.stop()
        self.slave1.join()
        self.slave2.stop()
        self.slave2.join()
        # Close TCP connections
        self.conn_client1.close()
        self.conn_client2.close()
        self.connexion.close()
        print("Server closed properly")
        
    

class ClientThread(Thread):
    def __init__(self, parent, conn_client, info_client):
        Thread.__init__(self)
        self.running = True
        self.parent = parent
        self.conn_client = conn_client
        self.info_client = info_client
        self.lastKeepAliveTime = time.time()


    def run(self):
        while self.running:
            datatoread, wlist, xlist = select.select([self.conn_client], [], [], 0.05)
            for data in datatoread:
                message = data.recv(1024)
                try:
                    message = pickle.loads(message)
                    if (message.type=='goal'):
                        self.goalReception(message)
                    elif (message.type=='rfid'):
                        self.RFIDReception(message)
                    elif (message.type=='keepalive'):
                        self.lastKeepAliveTime = time.time()
                except:
                    pass
            self.keepAlive()


    def goalReception(self, message):
        if message.replayLength != 0:
            self.conn_client.send("1".encode())
            buffersize=0
            with open(getContent("replay_received.mp4"), "wb") as video:
                while(buffersize<message.replayLength):
                    buffer = self.conn_client.recv(min(1024,message.replayLength-buffersize))
                    buffersize+=len(buffer)
                    video.write(buffer)
                    self.lastKeepAliveTime = time.time()
        else:
            conn_client.send("0".encode())
        self.parent.goalSignal.emit(message.getSide())


    def RFIDReception(self, message):
        self.parent.rfidSignal.emit(message.getSide(), message.getRFID())


    def keepAlive(self):
        if(time.time() - self.lastKeepAliveTime > 5):
            self.parent.clientLostSignal.emit("display", "Having connection troubles with client " + str(self.info_client) + 
            ". The window will automatically disapear once the client would have reconnected.")
            self.parent.connexion.listen(5)
            self.conn_client, self.info_client = self.parent.connexion.accept()
            print("Client reconnected " + str(self.conn_client))
            self.parent.clientLostSignal.emit("close", None)


    def stop(self):
        self.conn_client.close()
        self.running = False

