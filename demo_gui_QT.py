from GUI_QT import *
from Parameter_Input import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
# 继承至界面文件的主窗口类

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    # 创建启动界面，支持png透明图片
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('GUI_Start.jpg'))
    splash.show()

    # 可以显示启动信息
    splash.showMessage('正在加载……')
    time.sleep(1)
    # 关闭启动画面
    splash.close()
    myWin = MyMainWindow()
    child = QDialog()
    child_ui = Ui_Dialog()
    child_ui.setupUi(child)
    myWin.show()
    sys.exit(app.exec_())
