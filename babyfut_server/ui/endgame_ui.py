# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/endgame.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 693)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblTitle = QtWidgets.QLabel(Form)
        self.lblTitle.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lblTitle.setObjectName("lblTitle")
        self.verticalLayout.addWidget(self.lblTitle)
        spacerItem = QtWidgets.QSpacerItem(20, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.widgetLayoutP1 = QtWidgets.QWidget(Form)
        self.widgetLayoutP1.setObjectName("widgetLayoutP1")
        self.layoutP1 = QtWidgets.QVBoxLayout(self.widgetLayoutP1)
        self.layoutP1.setObjectName("layoutP1")
        self.imgP1 = QtWidgets.QWidget(self.widgetLayoutP1)
        self.imgP1.setMinimumSize(QtCore.QSize(400, 400))
        self.imgP1.setMaximumSize(QtCore.QSize(400, 400))
        self.imgP1.setBaseSize(QtCore.QSize(400, 400))
        self.imgP1.setStyleSheet("border-image: url(:/ui/img/placeholder_head.jpg);")
        self.imgP1.setObjectName("imgP1")
        self.layoutP1.addWidget(self.imgP1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutP1.addItem(spacerItem2)
        self.lblP1 = QtWidgets.QLabel(self.widgetLayoutP1)
        self.lblP1.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.lblP1.setFont(font)
        self.lblP1.setAlignment(QtCore.Qt.AlignCenter)
        self.lblP1.setObjectName("lblP1")
        self.layoutP1.addWidget(self.lblP1)
        self.horizontalLayout.addWidget(self.widgetLayoutP1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.widgetLayoutP2 = QtWidgets.QWidget(Form)
        self.widgetLayoutP2.setObjectName("widgetLayoutP2")
        self.layoutP2 = QtWidgets.QVBoxLayout(self.widgetLayoutP2)
        self.layoutP2.setObjectName("layoutP2")
        self.ImgP2 = QtWidgets.QWidget(self.widgetLayoutP2)
        self.ImgP2.setMinimumSize(QtCore.QSize(400, 400))
        self.ImgP2.setMaximumSize(QtCore.QSize(400, 400))
        self.ImgP2.setBaseSize(QtCore.QSize(400, 400))
        self.ImgP2.setStyleSheet("border-image: url(:/ui/img/placeholder_head.jpg);")
        self.ImgP2.setObjectName("ImgP2")
        self.layoutP2.addWidget(self.ImgP2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutP2.addItem(spacerItem4)
        self.lblP2 = QtWidgets.QLabel(self.widgetLayoutP2)
        self.lblP2.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.lblP2.setFont(font)
        self.lblP2.setAlignment(QtCore.Qt.AlignCenter)
        self.lblP2.setObjectName("lblP2")
        self.layoutP2.addWidget(self.lblP2)
        self.horizontalLayout.addWidget(self.widgetLayoutP2)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblTitle.setText(_translate("Form", "Congratulations!"))
        self.lblP1.setText(_translate("Form", "Player 1"))
        self.lblP2.setText(_translate("Form", "Player 2"))
from babyfut_server.ui import assets_rc
