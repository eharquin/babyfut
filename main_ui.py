# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 360)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(640, 360))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        MainWindow.setSizeIncrement(QtCore.QSize(1, 1))
        MainWindow.setBaseSize(QtCore.QSize(640, 360))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#centralWidget {border-image: url(:/img/bg0.jpg) 0 0 0 0 stretch stretch; }")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lcdTime = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdTime.sizePolicy().hasHeightForWidth())
        self.lcdTime.setSizePolicy(sizePolicy)
        self.lcdTime.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdTime.setDigitCount(8)
        self.lcdTime.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTime.setObjectName("lcdTime")
        self.horizontalLayout.addWidget(self.lcdTime)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.panels = QtWidgets.QStackedWidget(self.centralwidget)
        self.panels.setAutoFillBackground(False)
        self.panels.setObjectName("panels")
        self.verticalLayout.addWidget(self.panels)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.panels.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Babyfoot"))

import assets_rc
