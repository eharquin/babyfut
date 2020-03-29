# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
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
        self.centralwidget.setStyleSheet("#centralwidget {\n"
"    border-image: url(:/ui/img/bg/bg1.jpg) 0 0 0 0 stretch stretch; \n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutMenuBar = QtWidgets.QHBoxLayout()
        self.layoutMenuBar.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.layoutMenuBar.setObjectName("layoutMenuBar")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layoutMenuBar.addItem(spacerItem)
        self.lcdTime = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdTime.sizePolicy().hasHeightForWidth())
        self.lcdTime.setSizePolicy(sizePolicy)
        self.lcdTime.setMinimumSize(QtCore.QSize(100, 30))
        self.lcdTime.setStyleSheet("color: rgb(231, 231, 231);")
        self.lcdTime.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdTime.setDigitCount(8)
        self.lcdTime.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdTime.setObjectName("lcdTime")
        self.layoutMenuBar.addWidget(self.lcdTime)
        spacerItem1 = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.layoutMenuBar.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.layoutMenuBar)
        self.panels = QtWidgets.QStackedWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.panels.setFont(font)
        self.panels.setStyleSheet("* {\n"
"    color: rgb(229, 229, 229);\n"
"}\n"
"\n"
"QPushButton, QGroupBox {\n"
"    background-color: rgba(44, 44, 63, 150);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    background-color: rgba(44, 44, 63, 240);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.panels.setObjectName("panels")
        self.verticalLayout.addWidget(self.panels)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.panels.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Babyfoot"))
from babyfut_server.ui import assets_rc
