# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 727)
        Form.setStyleSheet("#btnScore1, #btnScore2 {\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 rgb(168, 170, 184));\n"
"color: black;\n"
" border-style: solid;\n"
" border-width:1px;\n"
" border-radius:14ex;\n"
" border-color: green;\n"
" max-width:200px;\n"
" max-height:200px;\n"
" min-width:200px;\n"
" min-height:200px;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnScore1 = QtWidgets.QPushButton(Form)
        self.btnScore1.setObjectName("btnScore1")
        self.horizontalLayout.addWidget(self.btnScore1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnScore2 = QtWidgets.QPushButton(Form)
        self.btnScore2.setObjectName("btnScore2")
        self.horizontalLayout.addWidget(self.btnScore2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem4)
        self.lcdChrono = QtWidgets.QLCDNumber(Form)
        self.lcdChrono.setMinimumSize(QtCore.QSize(0, 75))
        self.lcdChrono.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdChrono.setSmallDecimalPoint(False)
        self.lcdChrono.setDigitCount(8)
        self.lcdChrono.setObjectName("lcdChrono")
        self.verticalLayout.addWidget(self.lcdChrono)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.btnCancel = QtWidgets.QPushButton(Form)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnScore1.setText(_translate("Form", "0"))
        self.btnScore2.setText(_translate("Form", "0"))
        self.btnCancel.setText(_translate("Form", "Cancel"))

