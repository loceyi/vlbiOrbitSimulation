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
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))

        # self.statusBar = self.statusbar
        # self.statusBar.showMessage('菜单选项被点击了', 5000)
        # self.setWindowTitle('QStatusBar例子')

    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

#     def paintEvent1(self, event):
#
#
#     def keyPressEvent1(self,e):
#
#         if e.key() == Qt.Key_Escape:
#             self.close()
#
class ChildWindow(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self):
        super(ChildWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        self.pushButton.clicked.connect(self.showdialog)  # 按钮事件绑定

    def showdialog(self):

        dialog=QtWidgets.QDialog()
        # dialog.self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        dialog.setWindowTitle("Results")
        # dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.show()
#
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
    child_ui = ChildWindow()
    btn = myWin.pushButton
    btn.clicked.connect(child_ui.show)

    myWin.show()
    sys.exit(app.exec_())