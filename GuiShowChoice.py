# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiShowChoice.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(810, 577)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 80, 211, 41))
        self.pushButton.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 160, 211, 41))
        self.pushButton_2.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 236, 211, 41))
        self.pushButton_3.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(60, 320, 211, 41))
        self.pushButton_4.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(690, 520, 61, 31))
        self.pushButton_5.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(410, 90, 231, 271))
        self.label.setStyleSheet("image: url(:/GUI_Image/background/satellite_net.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(440, 370, 211, 41))
        self.pushButton_6.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(440, 450, 211, 41))
        self.pushButton_7.setStyleSheet("font: 9pt \"Adobe 黑体 Std R\";")
        self.pushButton_7.setObjectName("pushButton_7")

        self.retranslateUi(Dialog)
        self.pushButton_5.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Result"))
        self.pushButton.setText(_translate("Dialog", "Orbit Elements Report"))
        self.pushButton_2.setText(_translate("Dialog", "3D Graph"))
        self.pushButton_3.setText(_translate("Dialog", "Observe time Report"))
        self.pushButton_4.setText(_translate("Dialog", "Access Report"))
        self.pushButton_5.setText(_translate("Dialog", "Exit"))
        self.pushButton_6.setText(_translate("Dialog", "Start Local Web Server"))
        self.pushButton_7.setText(_translate("Dialog", "Stop Local Web Server"))

import backgraound_rc
