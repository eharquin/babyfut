# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/delete_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 433)
        Dialog.setStyleSheet("color: rgb(52, 53, 77)")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblTitle = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setObjectName("lblTitle")
        self.verticalLayout.addWidget(self.lblTitle)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.lblMsg = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lblMsg.setFont(font)
        self.lblMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.lblMsg.setObjectName("lblMsg")
        self.verticalLayout.addWidget(self.lblMsg)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rbDeleteAll = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.rbDeleteAll.setFont(font)
        self.rbDeleteAll.setChecked(True)
        self.rbDeleteAll.setObjectName("rbDeleteAll")
        self.horizontalLayout.addWidget(self.rbDeleteAll)
        self.rbDeletePicture = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.rbDeletePicture.setFont(font)
        self.rbDeletePicture.setObjectName("rbDeletePicture")
        self.horizontalLayout.addWidget(self.rbDeletePicture)
        self.rbHideAccount = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.rbHideAccount.setFont(font)
        self.rbHideAccount.setObjectName("rbHideAccount")
        self.horizontalLayout.addWidget(self.rbHideAccount)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.rbDeleteAll, self.rbDeletePicture)
        Dialog.setTabOrder(self.rbDeletePicture, self.rbHideAccount)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lblTitle.setText(_translate("Dialog", "Changing {}\'s profile"))
        self.lblMsg.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Select an option<br/>then validate by passing your badge on the table</p></body></html>"))
        self.rbDeleteAll.setText(_translate("Dialog", "Delete all records"))
        self.rbDeletePicture.setText(_translate("Dialog", "Remove the Picture"))
        self.rbHideAccount.setText(_translate("Dialog", "Make the accout private"))
