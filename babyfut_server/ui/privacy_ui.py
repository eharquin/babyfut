# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/privacy.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 720)
        Form.setStyleSheet("QRadioButton {\n"
"    border: 2px solid rgb(74, 74, 107);\n"
"    border-radius: 10px;\n"
"    border-color: rgb(74, 74, 107);\n"
"}\n"
"\n"
"QRadioButton::checked {\n"
"    background-color: rgba(44, 44, 63, 240);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    background-color: transparent;\n"
"    border: 0px solid transparent;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(15, 15, 15, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.txtPrivacy = QtWidgets.QTextEdit(Form)
        self.txtPrivacy.setStyleSheet("color: rgb(56, 56, 56);")
        self.txtPrivacy.setReadOnly(True)
        self.txtPrivacy.setObjectName("txtPrivacy")
        self.verticalLayout.addWidget(self.txtPrivacy)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Privacy"))
from babyfut_server.ui import assets_rc
