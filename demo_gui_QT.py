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
from datetime import datetime
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
        self.pushButton.clicked.connect(self.run_simulation)  # 按钮事件绑定


    def run_simulation(self):
        Start_Time,Number_Of_Steps, Step_Size, Semimajor_Axis,\
        Eccentricity, Inclination, Perigee, RAAN, TA=self.Initial_Value_Get()






        self.showdialog()


    def showdialog(self):

        dialog=QtWidgets.QDialog()
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        dialog.resize(screen.width(),screen.height())
        dialog.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        dialog.setWindowTitle("Results")
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def Initial_Value_Get(self):


        import re

        from math import floor


        Start_Time_str = self.Start_Time.text()
        Stop_Time_str = self.Stop_Time.text()
        Step_Size_str = self.Step_Size.text()
        Coord_System_str = self.Coord_System.currentText()
        Semimajor_Axis_str = self.Semimajor_Axis.text()
        Eccentricity_str = self.Eccentricity.text()
        Inclination_str = self.Inclination.text()
        Perigee_str = self.Perigee.text()
        RAAN_str=self.RAAN.text()
        TA_str = self.TA.text()

        #Start time
        Start_Time_Seconds=int(Start_Time_str[0:2])
        Start_Time_Mins=int(Start_Time_str[3:5])
        Start_Time_Hrs = int(Start_Time_str[6:8])
        Start_Time_Day = int(Start_Time_str[9:11])
        Start_Time_Month = int(Start_Time_str[12:14])
        Start_Time_Year = int(Start_Time_str[15:19])


        #Stop time
        Stop_Time_Seconds = int(Stop_Time_str[0:2])
        Stop_Time_Mins = int(Stop_Time_str[3:5])
        Stop_Time_Hrs = int(Stop_Time_str[6:8])
        Stop_Time_Day = int(Stop_Time_str[9:11])
        Stop_Time_Month = int(Stop_Time_str[12:14])
        Stop_Time_Year = int(Stop_Time_str[15:19])



        #Step_Size
        Step_Size=float(re.search("(\d+(\.\d+)?)",Step_Size_str).group())


        # Number of Steps
        d1 = datetime(Start_Time_Year, Start_Time_Month, Start_Time_Day,
                               Start_Time_Hrs, Start_Time_Mins,Start_Time_Seconds)


        d2 = datetime(Stop_Time_Year, Stop_Time_Month, Stop_Time_Day ,
                               Stop_Time_Hrs, Stop_Time_Mins , Stop_Time_Seconds)
        interval = d2 - d1
        Total_Time = interval.days * 24 * 3600 + interval.seconds

        Number_Of_Steps=floor(Total_Time/Step_Size)





        #Semimajor_Axis

        Semimajor_Axis=float(re.search("(\d+(\.\d+)?)",Semimajor_Axis_str).group())

        # Eccentricity

        Eccentricity = float(re.search("(\d+(\.\d+)?)",Eccentricity_str).group())


        #Inclination

        Inclination = float(re.search("(\d+(\.\d+)?)",Inclination_str).group())

        # Perigee

        Perigee = float(re.search("(\d+(\.\d+)?)",Perigee_str).group())

        # RAAN

        RAAN = float(re.search("(\d+(\.\d+)?)",RAAN_str).group())


        #TA

        TA = float(re.search("(\d+(\.\d+)?)",TA_str).group())








        Start_Time=[Start_Time_Seconds,Start_Time_Mins,Start_Time_Hrs,
                    Start_Time_Day,Start_Time_Month,Start_Time_Year]



        return Start_Time,Number_Of_Steps,Step_Size,Semimajor_Axis,\
               Eccentricity,Inclination,Perigee,RAAN,TA









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