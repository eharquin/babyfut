#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Laurine Dictus, Anaël Lacour
"""

import threading, socket

hote = ''
port = 12800

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((hote, port))
        self.connexion.listen()
        print("Waiting for connection with client\n")
        self.connexion_client, self.infos_connexion = self.connexion.accept()
        print("Connection established with client\n")

    def bytetoArray(self, bite):
    	res=0
    	for i in range(4):
    		res += bite[i]<<(i*8)
    	return res

    def run(self):
        while 1:
            msg_receive = self.connexion_client.recv(4)
            currentsize=0
            try:
                print("reception du replay")
                sizetoHave = self.bytetoArray(msg_receive)
                print("\tsizeToHave ", sizetoHave);
                with open('../../content/Replay Right.mp4', "wb") as video:
                    i = 0
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
                            i += 1
                            currentsize += 1024
                    print("fin de reception..")
                    #n +=1
            except :
                print("erreur reception")
        self.__close__()

    def closeConn(self):
        self.connexion_client.send("FIN".encode())
        self.__close__()

    def stop(self):
        self._running = False

    def __close__(self):
        print("Connection stoped\n")
        self.connexion_client.close()
        self.connexion.close()
