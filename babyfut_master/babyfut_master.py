#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Antoine Lima, Leo Reynaert, Domitille Jehenne
@modifs : Laurine Dictus, Anaël Lacour
@modifs : Yoann Malot, Thibaud Le Graverend
@modifs : Yaathavan Kumarasamy
"""

from multiprocessing.connection import wait
import os
from os.path import dirname, abspath, join, exists
import glob
import sys
import logging

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

'''Global function which returns the path of the content folder'''
def getContent(path):
    contentFolder = join(dirname(dirname(abspath(__file__))), 'content')
    return join(contentFolder, path)

'''Global function to find the (open) QMainWindow in application'''
def getMainWin():
    from .ui.mainwin import MainWin
    for widget in QApplication.instance().topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None

ON_RASP = (os.uname()[1] == 'master')
IMG_PATH = getContent('img')


if __name__=='__main__':
    __package__ = 'babyfut_master'
    from .ui.mainwin import MainWin
    from .modules import GameModule
    from common.side import Side
    from .core.input import Input
    from .core.database import Database
    #from .core.server import Server

    try:
        #logging.basicConfig(filename='babyfoot.log', level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)

        #Create the App and the MainWindow
        app = QApplication(sys.argv)
        myapp = MainWin()

        if not exists(IMG_PATH):
             os.makedirs(IMG_PATH)
        
        #Creates instance of DB
        db = Database.instance()
        #Creates an Input object to connect joystick and buttons
        input = Input()

        # creates thread that deals w/ client connection etc.
        myapp.connect_slaves()

        myapp.show()
        app.exec_()

    finally:
        myapp.stop()
        Database.instance().close()
        # for f in glob.glob(join(IMG_PATH, '*')):
        # 	os.remove(f)
