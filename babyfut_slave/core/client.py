#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import threading, socket, sys, os, time

hote = '169.254.11.5' #pour tester en local, sinon remplacer par l'ip de la rasp maitre
port = 12800

class Client(threading.Thread):
    def __init__(self, replay):
        """ Initialisation de la classe """
        threading.Thread.__init__(self)
        self.connexion = socket.socket()
        self.threadReplay = replay


    def convertbyte(self, no):
    	result=bytearray()
    	result.append(no &255 )
    	for i in range(3):
    		no = no >>8
    		result.append(no & 255)
    	return result

    def run(self):
        while 1:
            #msg_recu = self.connexion.recv(1024).decode()
            #print(msg_recu)
            #if msg_recu == "" or msg_recu == "FIN":
                #print("connection coupee car message recu: " + msg_recu)
            #    break
            #else:
            #    print(msg_recu)
            time.sleep(0.01)
        self.connexion.close()
        print("connexion fermee\n")

    def send(self):
        self.threadReplay.stop_recording()
        self.connexion.connect((hote, port))
        print("connexion etablie\n")
        print("envoie replay")
        if os.path.exists("replay.mp4"):
        	length=os.path.getsize("replay.mp4")
        	#print(length)
        	self.connexion.send(self.convertbyte(length))
        with open("replay.mp4", "rb") as video:
        #with open("/home/pi/pr_baby/content/Replay Right.mp4", "rb") as video:
            buffer = video.read()
            self.connexion.sendall(buffer)

        print("tout est envoyé ")
        time.sleep(2)
        self.threadReplay.start_recording()


    def stop(self):
        self._running = False