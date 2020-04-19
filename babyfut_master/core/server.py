#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
@modif : Thibaud Le Graverend
"""

import threading, socket, pickle, time
import _thread


from PyQt5.QtCore import QObject, pyqtSignal
from ..babyfut_master import ON_RASP, getContent
from common.side import Side, opposite
from common.settings import Settings
from common.message import Message

if ON_RASP:
	import RPi.GPIO as GPIO
	from pirc522 import RFID # PyPi library
	import pyautogui # PyPi library


host = ''
port = 15555

class Server(QObject):

    # Signals for goal and rfid detection
    goalSignal = pyqtSignal(Side)
    rfidSignal = pyqtSignal(Side, str)

    def __init__(self):
        QObject.__init__(self)
        #threading.Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((host, port))
        print("Serveur instancié\n")

        # Wait for connection with 1st slave
        self.connexion.listen(5)
        self.conn_client1, self.info_client1 = self.connexion.accept()
        print("Connexion établi avec client1" + str(self.conn_client1) + str(self.info_client1))
        self.slave1 = _thread.start_new_thread(self.client_thread, (self.conn_client1, self.info_client1))

        # Wait for 2nd slave
        self.connexion.listen(5)
        self.conn_client2, self.info_client2 = self.connexion.accept()
        print("Connexion établi avec client2" + str(self.conn_client2) + str(self.info_client2))
        self.slave2 = _thread.start_new_thread(self.client_thread, (self.conn_client2, self.info_client2))


    def goalReception(self, message, conn_client):
        self.goalSignal.emit(message.getSide()) # TODO handle signal
        print("But marqué !")
        conn_client.send("1".encode())
        buffersize=0
        with open(getContent("videorec.mp4"), "wb") as video:
            while(buffersize<message.replayLength):
                buffer = conn_client.recv(1024)
                time.sleep(5/600)
                buffersize+=len(buffer)
                video.write(buffer)
            print("vid ok")



    def RFIDReception(self, message):
        self.rfidSignal.emit(message.getSide(), message.getRFID()) # TODO handle signal


    def client_thread(self, conn_client, info_client):
        while 1:
            message = conn_client.recv(1024)
            message = pickle.loads(message)
            if (message.type=='goal'):
                print("Goal, appel de la fonction")
                self.goalReception(message, conn_client)
            elif (message.type=='rfid'):
                self.RFIDReception(message)
            else:
                pass

        
    







    # goalDetected = pyqtSignal(Side)

    # def __init__(self):
    #     QObject.__init__(self)
    #     threading.Thread.__init__(self)
    #     self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.connexion.bind((hote, port))
    #     self.connexion.listen()
    #     if ON_RASP:
    #         self.side = Side.Left if Settings['app.side']=='left' else Side.Right
    #         self.side = opposite(self.side)
    #     print("Waiting for connection with client\n")

    # def bytetoArray(self, bite):
    # 	res=0
    # 	for i in range(4):
    # 		res += bite[i]<<(i*8)
    # 	return res

    # def run(self):
    #     while 1:
    #         self.connexion_client, self.infos_connexion = self.connexion.accept()
    #         print("Connection established with client\n")
    #         msg_receive = self.connexion_client.recv(4)
    #         currentsize=0
    #         print("reception taille replay")
    #         sizetoHave = self.bytetoArray(msg_receive)
    #         print("\tsizeToHave ", sizetoHave);
    #         with open('./content/Replay Right.mp4', "wb") as video:
    #             print("reception du replay")
    #             while sizetoHave > currentsize:
    #                 buffer = self.connexion_client.recv(1024)
    #                 if not buffer :
    #                     break
    #                 if len(buffer) + currentsize >= sizetoHave:
    #                     #print("len buffer ", len(buffer))
    #                     video.write(buffer)
    #                     currentsize += len(buffer)
    #                     print(currentsize)
    #                 else:
    #                     video.write(buffer)
    #                     #print(currentsize)
    #                     currentsize += 1024
    #             print("fin de reception..")
    #             if ON_RASP:
    #                 self.goalDetected.emit(self.side)
    #                 print("envoie signal OK")
    #         self.connexion_client.close()
    #     self.__close__()

    # def closeConn(self):
    #     self.connexion_client.send("FIN".encode())
    #     self.__close__()

    # def stop(self):
    #     self._running = False

    # def __close__(self):
    #     print("Connection stoped\n")
    #     self.connexion.close()
