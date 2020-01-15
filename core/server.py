#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import threading, socket
from Babyfut.core.player import Side
from Babyfut.core.settings import Settings

hote = ''
port = 12800

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((hote, port))
        self.connexion.listen()
        self.side = Side.Left if Settings['app.side']=='left' else Side.Right
        self.side.opposite()
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
            time.sleep(0.5)
            msg_receive = self.connexion_client.recv(4)
            currentsize=0
            print("reception taille replay")
            sizetoHave = self.bytetoArray(msg_receive)
            print("\tsizeToHave ", sizetoHave);
            try:
                with open('./content/Replay Right.mp4', "wb") as video:
                    #print("fichier ouvert")
                    i = 0
                    #print(i)
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
                            i+=1
                        else:
                            video.write(buffer)
                            #print(currentsize)
                            i += 1
                            currentsize += 1024
                    print("fin de reception..")
                    pyqtSignal(self.side)
                    #n +=1
            except :
                print("erreur reception")
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
