# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(728, 540)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 712, 482))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.options = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.options.setShowGrid(True)
        self.options.setObjectName("options")
        self.options.setColumnCount(2)
        self.options.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.options.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.options.setHorizontalHeaderItem(1, item)
        self.options.horizontalHeader().setVisible(True)
        self.options.horizontalHeader().setStretchLastSection(True)
        self.options.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.options)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnSave = QtWidgets.QPushButton(Form)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.btnBack = QtWidgets.QPushButton(Form)
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout.addWidget(self.btnBack)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.options.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name"))
        item = self.options.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Value"))
        self.btnSave.setText(_translate("Form", "Save"))
        self.btnBack.setText(_translate("Form", "Back"))

import assets_rc
