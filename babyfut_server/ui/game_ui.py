# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/game.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 720)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnScore1 = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnScore1.sizePolicy().hasHeightForWidth())
        self.btnScore1.setSizePolicy(sizePolicy)
        self.btnScore1.setMinimumSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setPointSize(70)
        self.btnScore1.setFont(font)
        self.btnScore1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnScore1.setObjectName("btnScore1")
        self.horizontalLayout.addWidget(self.btnScore1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btnScore2 = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnScore2.sizePolicy().hasHeightForWidth())
        self.btnScore2.setSizePolicy(sizePolicy)
        self.btnScore2.setMinimumSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setPointSize(70)
        self.btnScore2.setFont(font)
        self.btnScore2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnScore2.setObjectName("btnScore2")
        self.horizontalLayout.addWidget(self.btnScore2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.lcdChrono = QtWidgets.QLCDNumber(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdChrono.sizePolicy().hasHeightForWidth())
        self.lcdChrono.setSizePolicy(sizePolicy)
        self.lcdChrono.setMinimumSize(QtCore.QSize(200, 80))
        self.lcdChrono.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdChrono.setDigitCount(8)
        self.lcdChrono.setObjectName("lcdChrono")
        self.verticalLayout.addWidget(self.lcdChrono)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnScore1.setText(_translate("Form", "0"))
        self.btnScore2.setText(_translate("Form", "0"))
