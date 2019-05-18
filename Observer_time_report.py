# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Observer_time_report.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(633, 420)
        self.Step_Size_2 = QtWidgets.QLineEdit(Dialog)
        self.Step_Size_2.setGeometry(QtCore.QRect(340, 60, 221, 41))
        self.Step_Size_2.setObjectName("Step_Size_2")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(40, 60, 291, 41))
        self.label_12.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.label_12.setObjectName("label_12")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(450, 340, 131, 41))
        self.pushButton.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Observe Time Report"))
        self.Step_Size_2.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.Step_Size_2.setText(_translate("Dialog", "(1,1,1)"))
        self.label_12.setText(_translate("Dialog", "Observed Target Direction:"))
        self.pushButton.setText(_translate("Dialog", "Compute"))

