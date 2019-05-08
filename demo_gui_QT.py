# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_gui_QT.py'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from GUI_QT import *
from Parameter_Input import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
# 继承至界面文件的主窗口类

class MyMainWindow(QtWidgets.QMainWindow, Ui_VSS):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


#     def paintEvent1(self, event):
#
#
#     def keyPressEvent1(self,e):
#
#         if e.key() == Qt.Key_Escape:
#             self.close()
#
# class ChildWindow(QtWidgets.QDialog, Ui_Dialog):
#
#     def __init__(self):
#         super(ChildWindow,self).__init__()
#         self.setupUi(self)
#
#         self.setWindowTitle('child window')
#
#         self.pushButton.clicked.connect( self.btnClick)  #按钮事件绑定
#
#     def btnClick(self):
# #子窗体自定义事件
#         self.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    # 创建启动界面，支持png透明图片
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('bfr.jpg'))
    splash.show()

    # 可以显示启动信息
    splash.showMessage('正在加载……')
    time.sleep(1)
    # 关闭启动画面
    splash.close()
    myWin = MyMainWindow()
    child = QtWidgets.QDialog()
    child_ui = Ui_Dialog()
    child_ui.setupUi(child)
    btn = myWin.pushButton
    btn.clicked.connect(child.show)

    myWin.show()
    sys.exit(app.exec_())