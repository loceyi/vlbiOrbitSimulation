# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_QT.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VSS(object):
    def setupUi(self, VSS):
        VSS.setObjectName("VSS")
        VSS.resize(800, 408)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VSS.sizePolicy().hasHeightForWidth())
        VSS.setSizePolicy(sizePolicy)
        VSS.setMinimumSize(QtCore.QSize(800, 390))
        VSS.setAutoFillBackground(False)
        VSS.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-image: url(:/GUI_Image/background/wall-ocisly.png);\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(VSS)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 290, 171, 61))
        self.pushButton.setStyleSheet("border-color: rgb(255, 255, 246);\n"
"background-color: rgb(29, 29, 29);\n"
"color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 290, 171, 61))
        self.pushButton_2.setStyleSheet("border-color: rgb(255, 255, 246);\n"
"background-color: rgb(29, 29, 29);\n"
"color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        VSS.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(VSS)
        self.statusbar.setObjectName("statusbar")
        VSS.setStatusBar(self.statusbar)
        self.actionadf = QtWidgets.QAction(VSS)
        self.actionadf.setObjectName("actionadf")

        self.retranslateUi(VSS)
        QtCore.QMetaObject.connectSlotsByName(VSS)

    def retranslateUi(self, VSS):
        _translate = QtCore.QCoreApplication.translate
        VSS.setWindowTitle(_translate("VSS", "VSS  Version 1.0"))
        VSS.setWhatsThis(_translate("VSS", "<html><head/><body><p><img src=\":/GUI_Image/background/earth.jpg\"/></p></body></html>"))
        self.pushButton.setText(_translate("VSS", "建立新的仿真"))
        self.pushButton_2.setText(_translate("VSS", "退出"))
        self.actionadf.setText(_translate("VSS", "Build New Satellite Object"))

import backgraound_rc
