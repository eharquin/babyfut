# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(813, 463)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.btn0Start = QtWidgets.QPushButton(Form)
        self.btn0Start.setAutoDefault(True)
        self.btn0Start.setDefault(True)
        self.btn0Start.setObjectName("btn0Start")
        self.verticalLayout.addWidget(self.btn0Start)
        spacerItem3 = QtWidgets.QSpacerItem(20, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.btn1Options = QtWidgets.QPushButton(Form)
        self.btn1Options.setObjectName("btn1Options")
        self.verticalLayout.addWidget(self.btn1Options)
        self.btn2Exit = QtWidgets.QPushButton(Form)
        self.btn2Exit.setObjectName("btn2Exit")
        self.verticalLayout.addWidget(self.btn2Exit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn0Start.setText(_translate("Form", "Start"))
        self.btn1Options.setText(_translate("Form", "Options"))
        self.btn2Exit.setText(_translate("Form", "Exit"))

