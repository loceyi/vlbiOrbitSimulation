# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Access.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(633, 506)
        self.Step_Size_5 = QtWidgets.QLineEdit(Dialog)
        self.Step_Size_5.setGeometry(QtCore.QRect(320, 270, 211, 41))
        self.Step_Size_5.setObjectName("Step_Size_5")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(10, 130, 301, 41))
        self.label_14.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(10, 270, 301, 41))
        self.label_15.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.label_15.setObjectName("label_15")
        self.Step_Size_3 = QtWidgets.QLineEdit(Dialog)
        self.Step_Size_3.setGeometry(QtCore.QRect(320, 60, 211, 41))
        self.Step_Size_3.setObjectName("Step_Size_3")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(10, 60, 301, 41))
        self.label_13.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.label_13.setObjectName("label_13")
        self.Step_Size_4 = QtWidgets.QLineEdit(Dialog)
        self.Step_Size_4.setGeometry(QtCore.QRect(320, 130, 211, 41))
        self.Step_Size_4.setObjectName("Step_Size_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(230, 420, 131, 41))
        self.pushButton.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.pushButton.setObjectName("pushButton")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(10, 200, 301, 41))
        self.label_16.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.label_16.setObjectName("label_16")
        self.Step_Size_6 = QtWidgets.QLineEdit(Dialog)
        self.Step_Size_6.setGeometry(QtCore.QRect(320, 200, 211, 41))
        self.Step_Size_6.setObjectName("Step_Size_6")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 420, 131, 41))
        self.pushButton_2.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Access"))
        self.Step_Size_5.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.Step_Size_5.setText(_translate("Dialog", "45 deg"))
        self.label_14.setText(_translate("Dialog", "Latitude(Ground Station):"))
        self.label_15.setText(_translate("Dialog", "MAX ElevationAngle:"))
        self.Step_Size_3.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.Step_Size_3.setText(_translate("Dialog", "45 deg"))
        self.label_13.setText(_translate("Dialog", "Longitude(Ground Station):"))
        self.Step_Size_4.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.Step_Size_4.setText(_translate("Dialog", "45 deg"))
        self.pushButton.setText(_translate("Dialog", "Compute"))
        self.label_16.setText(_translate("Dialog", "Altitude(Ground Station)"))
        self.Step_Size_6.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.Step_Size_6.setText(_translate("Dialog", "0 m"))
        self.pushButton_2.setText(_translate("Dialog", "Show"))

