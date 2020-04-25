#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Thibaud Le Graverend, Yoann Malot
"""

import socket, pickle, time, select
from PyQt5.QtCore import QObject
import os
import logging
from common.message import *
from ..babyfut_slave import getContent, ON_RASP
from threading import Event, Thread
from .replay import Replay

class Client(QObject):
    def __init__(self, host, port):
        QObject.__init__(self)
        self.replayPath = getContent("replay.mp4")
        self.replayReady = Event()
        self.replayReady.clear()

        self.host = host
        self.port = port

        self.socketToken = Event()
        self.socketToken.set()

        self.connect()


    def connect(self):
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = 0
        while not connected:
            try:
                self.connexion.connect((self.host, self.port))
                connected = 1
                print("Client connected")
                self.keepalive = KeepAlive(self)
                self.keepalive.start()
            except ConnectionError:
                print("Unreachable server, trying again in 2 seconds")
                time.sleep(3)


    def sendMessage(self, message):
        data = pickle.dumps(message)
        try:
            self.connexion.send(data)
        except OSError as Error:
            logging.debug(str(Error))


    def sendGoal(self):
        #If a Replay is found for sending
        #if (Replay.isCamAvailable() and os.path.exists(self.replayPath):
        if os.path.exists(self.replayPath):
            print("OK")
            if ON_RASP:
                self.replayReady.wait() #Flag set by ReplayThread when copy into replayPath is over
            length=os.path.getsize(self.replayPath)
            self.sendMessage(MessageGoal(length))
            wantReplay=self.connexion.recv(1) #Waiting order for sending replay
            if wantReplay.decode() == '1':
                self.sendReplay()
        else:
            self.sendMessage(MessageGoal(0))


    def sendRFID(self, rfid):
        self.sendMessage(MessageRFID(rfid))

    def setReplayReady(self):
        #Slot of the Replay Thread Signal 
        self.replayReady.set()

    def sendReplay(self):    
        self.socketToken.clear()    
        with open(self.replayPath, "rb") as video:
            buffer = video.read()
            self.connexion.sendall(buffer)
        self.socketToken.set()


    def stop(self):
        self.connexion.close()



class KeepAlive(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.running = True
        self.parent = parent


    def run(self):
        while self.running:
            if not self.parent.socketToken.isSet():
                self.parent.socketToken.wait()
            try:
                self.parent.connexion.send(pickle.dumps(MessageKeepAlive()))
            except OSError as error:
                print(str(error))
                self.parent.connexion.close()
                self.parent.connect()
                self.stop()
            time.sleep(1)


    def stop(self):
        self.running = False