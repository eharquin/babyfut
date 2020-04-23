#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import socket, pickle, time, select
from PyQt5.QtCore import QObject
import os
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

        self.connect()


    def connect(self):
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = 0
        while not connected:
            try:
                self.connexion.connect((self.host, self.port))
                connected = 1
                print("Client connected")
                self.keepalive = KeepAlive(self, self.connexion)
                self.keepalive.run()
            except ConnectionError:
                print("Unreachable server, trying again in 2 seconds")
                time.sleep(2)



    def sendMessage(self, message):
        data = pickle.dumps(message)
        self.connexion.send(data)


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
        with open(self.replayPath, "rb") as video:
            buffer = video.read()
            self.connexion.sendall(buffer)

    def sendKeepAlive(self):
        self.sendMessage(MessageKeepAlive())

    def stop(self):
        self.connexion.close()


class KeepAlive(Thread):
    def __init__(self, parent, connexion):
        self.running = True
        self.parent = parent
        self.connexion = connexion
        self.time = time.time()

    def run(self):
        disconnected = 0
        while self.running:
            datatoread, wlist, xlist = select.select([self.connexion], [], [], 0.5)
            for data in datatoread:
                message = data.recv(1024)
                message = pickle.loads(message)
                if (message.type=='keepalive'):
                    print("Keepalive reçu")
                    self.datetime = datetime.now()
            if (time.time()-self.time > 3):
                self.parent.connexion.close()
                self.parent.connect()
                self.stop()

    def stop(self):
        self.running = False