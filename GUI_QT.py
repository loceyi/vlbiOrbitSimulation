# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_QT.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 438)
        MainWindow.setStyleSheet("background-image: url(:/GUI_Image/background/earth.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 260, 41, 9))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 290, 111, 20))
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(5, 9, 20);\n"
"selection-color: rgb(5, 9, 20);\n"
"gridline-color: rgb(6, 10, 21);\n"
"border-top-color: rgb(5, 9, 20);\n"
"")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 290, 61, 21))
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 391, 41))
        self.label_2.setStyleSheet("background-color: rgb(4, 10, 24);\n"
"background-color: rgb(9, 22, 41);\n"
"alternate-background-color: rgb(3, 12, 29);\n"
"color: rgb(23, 62, 121);")
        self.label_2.setObjectName("label_2")
        self.label.raise_()
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><img src=\":/GUI_Image/background/earth.jpg\"/></p></body></html>"))
        self.pushButton.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">创建一个新的仿真对象</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "创建一个新的仿真对象"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))
        self.label_2.setWhatsThis(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">空间VLBI卫星仿真</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:16pt;\">空间VLBI卫星轨道仿真</span></p><p align=\"justify\"><br/></p></body></html>"))

import backgraound_rc
