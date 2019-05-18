# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_gui_QT.py'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from Visibility_for_Star import *
from Julian_date import Julian_date
from Ground_Station_Access import GSA
import Observe
import Access
import Observer_time_report
import GUI_QT
import Parameter_Input
import GuiShowChoice
import Graph
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from datetime import datetime
import numpy as np
from HPOP import HPOP
from CZML_Generate import CZML_Generate
from PyQt5.QtWebEngineWidgets import *
import Web_Server
import webbrowser
from sklearn.externals import joblib
import pyqtgraph as pg
from RV_To_Orbit_Elements import rv_to_orbit_element
from math import pi
import threading

# 继承至界面文件的主窗口类

class MyMainWindow(QtWidgets.QMainWindow, GUI_QT.Ui_VSS):
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
class ChildWindow(QtWidgets.QDialog, Parameter_Input.Ui_Dialog):

    def __init__(self):
        super(ChildWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        self.pushButton.clicked.connect(self.run_simulation)  # 按钮事件绑定


    def run_simulation(self):
        Start_Time, Stop_Time, Number_Of_Steps, Step_Size, Initial_Orbit_Elements=self.Initial_Value_Get()
        joblib.dump(Start_Time, 'Start_Time.pkl')
        joblib.dump(Step_Size, 'Step_Size.pkl')
        joblib.dump(Number_Of_Steps, 'Number_Of_Steps.pkl')

        HPOP(Start_Time,Number_Of_Steps,Step_Size,Initial_Orbit_Elements)

        HPOP_Results= joblib.load('HPOP_Results.pkl')

        Start_time = "%s-%02d-%02dT%02d:%02d:%02dZ"%(Start_Time[5],Start_Time[4],Start_Time[3],Start_Time[2],
                                           Start_Time[1],Start_Time[0])
        end_time = "%s-%02d-%02dT%02d:%02d:%02dZ"%(Stop_Time[5],Stop_Time[4],Stop_Time[3],Stop_Time[2],
                                           Stop_Time[1],Stop_Time[0])
        # Start_time = "2012-03-15T10:00:00Z"
        # end_time = "2012-03-16T10:00:00Z"

        x = HPOP_Results[1, :]
        y = HPOP_Results[2, :]
        z = HPOP_Results[3, :]
        time=HPOP_Results[0,:]
        time = time.tolist()
        cartesian_file = []
        for i in range(0, len(time)):
            cartesian_file.append(time[i])
            cartesian_file.append(x[i])
            cartesian_file.append(y[i])
            cartesian_file.append(z[i])

        CZML_Generate(Start_time, end_time, cartesian_file)



        # self.showdialog()



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

        #Initial Orbit Elements

        Initial_Orbit_Elements = np.array([Semimajor_Axis, Eccentricity , Inclination,
                                           Perigee, RAAN, TA])  # 输入角度单位为度°








        Start_Time=[Start_Time_Seconds,Start_Time_Mins,Start_Time_Hrs,
                    Start_Time_Day,Start_Time_Month,Start_Time_Year]

        Stop_Time=[Stop_Time_Seconds,Stop_Time_Mins,Stop_Time_Hrs,
                    Stop_Time_Day,Stop_Time_Month,Stop_Time_Year]





        return Start_Time,Stop_Time,Number_Of_Steps,Step_Size,Initial_Orbit_Elements



# class showdialog(QtWidgets.QDialog):
#
#     def __init__(self):
#         super(showdialog,self).__init__()
#
#         # dialog=QtWidgets.QDialog()
#         self.btn1 = QtWidgets.QPushButton('Orbit Elements Report',self)
#         self.btn1.move(50, 50)
#         self.btn2 = QtWidgets.QPushButton('3D Graph',self)
#         self.btn2.move(50, 100)
#         self.btn2.setObjectName("btn2")
#         self.btn3 = QtWidgets.QPushButton('Observe time Report',self)
#         self.btn3.setObjectName("btn3")
#         self.btn3.move(50, 150)
#         self.btn4 = QtWidgets.QPushButton('Access Report',self)
#         self.btn4.move(50, 200)
#         screen = QtWidgets.QDesktopWidget().screenGeometry()
#         self.resize(screen.width(),screen.height())
#         self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
#         self.setWindowTitle("Results")
#         self.setWindowModality(QtCore.Qt.ApplicationModal)





class MainWindow2(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow2, self).__init__()
        # self.setWindowTitle('加载本地网页的例子')
        # self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        self.setGeometry(5, 30, 1355, 730)
        self.browser = QWebEngineView()
        # self.thread = threading.Thread(target=run, args=())
        # self.thread.setDaemon(True)
        # self.thread.start()
        # #加载外部的web界面
        url="http://localhost:9090/"
        self.browser.load(QtCore.QUrl(url))
        self.setCentralWidget(self.browser)








class GuishowChoice(QtWidgets.QDialog,GuiShowChoice.Ui_Dialog):
    def __init__(self, parent=None):
        super(GuishowChoice, self).__init__(parent)
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


class Thread(QtCore.QThread):


    def __init__(self):
        super().__init__()

    def run(self):

        Web_Server.GUI_Show()

    # 创建一个新的线程

class OpenWeb:


    def __init__(self):
        super().__init__()

    def run(self):

        webbrowser.open("http://localhost:9090/")


class MyGraphWindow(QtWidgets.QMainWindow, Graph.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyGraphWindow, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        # plt1, plt2, plt3, plt4, plt5, plt6=self.Get_graph()

        # self.verticalLayout_1.addWidget(plt1)
        # self.verticalLayout_2.addWidget(plt2)
        # self.verticalLayout_3.addWidget(plt3)
        # self.verticalLayout_4.addWidget(plt4)
        # self.verticalLayout_5.addWidget(plt5)
        # self.verticalLayout_6.addWidget(plt6)


    def Get_graph(self):

        Results = joblib.load('HPOP_Results.pkl')


        time = Results[0, :]
        x = Results[1, :]
        y = Results[2, :]
        z = Results[3, :]
        vx=Results[4,:]
        vy=Results[5,:]
        vz=Results[6,:]


        length = len(x)

        orbit_element_data = np.zeros([6,length])

        for i in range(1,length+1):

            temp=rv_to_orbit_element(np.array([x[i-1],y[i-1],z[i-1]]),
                                     np.array([vx[i-1],vy[i-1],vz[i-1]]),398600.4418e9)

            orbit_element_data[0,i-1]=temp[0]
            orbit_element_data[1, i - 1] =temp[1]
            orbit_element_data[2, i - 1] =temp[2]
            orbit_element_data[3, i - 1] =temp[3]
            orbit_element_data[4, i - 1] =temp[4]
            orbit_element_data[5, i - 1] =temp[5]




        plt1 = pg.PlotWidget(title="Semi-axis")
        plt1.plot(time, orbit_element_data[0,:])

        plt2 = pg.PlotWidget(title="Eccentricity")
        plt2.plot(time, orbit_element_data[1, :])

        plt3 = pg.PlotWidget(title="Inclination")
        plt3.plot(time, orbit_element_data[2, :])

        plt4 = pg.PlotWidget(title="RAAN")
        plt4.plot(time, orbit_element_data[3, :])

        plt5 = pg.PlotWidget(title="Perigee")
        plt5.plot(time, orbit_element_data[4, :])

        plt6 = pg.PlotWidget(title="True Anomaly")
        plt6.plot(time, orbit_element_data[5, :]% (2 * pi))

        self.verticalLayout_1.addWidget(plt1)
        self.verticalLayout_2.addWidget(plt2)
        self.verticalLayout_3.addWidget(plt3)
        self.verticalLayout_4.addWidget(plt4)
        self.verticalLayout_5.addWidget(plt5)
        self.verticalLayout_6.addWidget(plt6)

        self.show()

        # return plt1,plt2,plt3,plt4,plt5,plt6

        return




    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)


class MyAccess(QtWidgets.QDialog,Access.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyAccess, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        self.pushButton.clicked.connect(self.run_Ob)

        # self.statusBar = self.statusbar
        # self.statusBar.showMessage('菜单选项被点击了', 5000)
        # self.setWindowTitle('QStatusBar例子')

    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)



    def run_Ob(self):

        Longitude, Latitude, MAX_ElevationAngle,Altitude =self.value_get()
        HPOP_Results = joblib.load('HPOP_Results.pkl')
        x = HPOP_Results[1, :]
        y = HPOP_Results[2, :]
        z = HPOP_Results[3, :]
        time = HPOP_Results[0, :]

        Start_Time = joblib.load('Start_Time.pkl')

        year = Start_Time[5]
        month = Start_Time[4]
        day = Start_Time[3]
        hour = Start_Time[2]
        minute = Start_Time[1]
        second = Start_Time[0]

        t_start_jd = Julian_date(year, month, day, hour, minute, second)

        MJD_UTC_Start = t_start_jd - 2400000.5


        Visibility_GS_SAT = []
        # np.arange(0, len(time), 1)
        i=0

        for t in time:

            Visibility_GS_SAT.append(GSA(np.array([x[i],y[i],z[i]]),
                                    t, Latitude, Longitude, Altitude, MAX_ElevationAngle,MJD_UTC_Start))

            i=i+1




        joblib.dump(time, 'time.pkl')
        joblib.dump(Visibility_GS_SAT, 'Visibility_GS_SAT.pkl')


        return










    def value_get(self):
        import re

        Longitude_str = self.Step_Size_3.text()
        Latitude_str=self.Step_Size_4.text()
        MAX_ElevationAngle_str=self.Step_Size_5.text()
        Altitude_str = self.Step_Size_5.text()

        Longitude = float(re.search("(\d+(\.\d+)?)", Longitude_str).group())
        Latitude = float(re.search("(\d+(\.\d+)?)", Latitude_str).group())
        MAX_ElevationAngle = float(re.search("(\d+(\.\d+)?)", MAX_ElevationAngle_str).group())
        Altitude = float(re.search("(\d+(\.\d+)?)", Altitude_str).group())






        return Longitude,Latitude,MAX_ElevationAngle,Altitude









class Access_graph(QtWidgets.QMainWindow,Observe.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Access_graph, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        # plt1=self.Get_graph()

        # self.verticalLayout.addWidget(plt1)



    def Get_graph(self):

        Visibility_GS_SAT = joblib.load('Visibility_GS_SAT.pkl')

        time= joblib.load('time.pkl')



        plt1 = pg.PlotWidget(title="Access_GS_SAT")
        plt1.plot(time, Visibility_GS_SAT)

        self.verticalLayout.addWidget(plt1)
        self.show()



        return plt1





    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)













class MyObserver_time_report(QtWidgets.QDialog,Observer_time_report.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyObserver_time_report, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        self.pushButton.clicked.connect(self.run_Ob)



        # self.statusBar = self.statusbar
        # self.statusBar.showMessage('菜单选项被点击了', 5000)
        # self.setWindowTitle('QStatusBar例子')

    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

    def run_Ob(self):

        Direction_Vector=self.value_get()
        HPOP_Results = joblib.load('HPOP_Results.pkl')
        x = HPOP_Results[1, :]
        y = HPOP_Results[2, :]
        z = HPOP_Results[3, :]
        time = HPOP_Results[0, :]
        position= np.row_stack((x, y))
        position = np.row_stack((position, z))
        Start_Time = joblib.load('Start_Time.pkl')
        Step_Size = joblib.load('Step_Size.pkl')
        Number_Of_Steps=joblib.load('Number_Of_Steps.pkl')

        year = Start_Time[5]
        month = Start_Time[4]
        day = Start_Time[3]
        hour = Start_Time[2]
        minute = Start_Time[1]
        second = Start_Time[0]

        length = Number_Of_Steps  # 设置步长
          # 生成长度为60的数组,要打1.0因为数组数据类型要为float，输入1则默认类型为int
        timeJD = np.arange(0, length, 1)
        Visibility = np.arange(0, length, 1)
        JD_Start=Julian_date(year, month, day, hour, minute, second)

        for i in range(0, length):  # 0~59,没有60

            timeJD[i] = JD_Start+i*Step_Size/86400

            Visibility[i] = Visibility_for_celestial_body(Direction_Vector,position[:,i], timeJD[i])


        joblib.dump(time, 'time.pkl')
        joblib.dump(Visibility, 'Visibility.pkl')


        return







    def value_get(self):
        import re

        Direction_Vector_str = self.Step_Size_2.text()

        Direction_Vector_list_str = re.findall(r'\b\d+\b', Direction_Vector_str)
        Direction_Vector_list = list(map(float, Direction_Vector_list_str))
        Direction_Vector_array=np.array(Direction_Vector_list)




        return Direction_Vector_array


class VisibilityGraphWindow(QtWidgets.QMainWindow,Observe.Ui_MainWindow):
    def __init__(self, parent=None):
        super(VisibilityGraphWindow, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowIcon(QtGui.QIcon('./GUI_Image/background/satellites_128px_1169478_easyicon.net.ico'))
        # plt1=self.Get_graph()

        # self.verticalLayout.addWidget(plt1)



    def Get_graph(self):

        Visibility = joblib.load('Visibility.pkl')

        time= joblib.load('time.pkl')



        plt1 = pg.PlotWidget(title="Visibility")
        plt1.plot(time, Visibility)

        self.verticalLayout.addWidget(plt1)
        self.show()



        return plt1





    def center(self):

        screen=QtWidgets.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)








# def web_server():
#
#         thread = threading.Thread(target=run, args=())
#         self.thread.setDaemon(True)
#         thread.start()
#
# def run():
#         # 线程相关代码
#         Web_Server.GUI_Show()

#
# class Thread(QtCore.QThread):
#
#
#     def __init__(self):
#         super().__init__()





    # 创建一个新的线程





    #
#
#     def btnClick(self):
# #子窗体自定义事件
#         self.close()

# def three_d_graph():
#     MainWin2 = MainWindow2()



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
    GuishowChoice_ui=GuishowChoice()
    OpenWeb_ui=OpenWeb()
    # showdialog_ui=showdialog()
    thread = Thread()
    Graph_ui=MyGraphWindow()
    Observer_time_report_ui=MyObserver_time_report()
    MainWin2 = MainWindow2()
    VisibilityGraphWindow_ui=VisibilityGraphWindow()
    MyAccess_ui=MyAccess()
    Access_graph_ui=Access_graph()
    # MainWin2=MainWindow2()
    btn = myWin.pushButton
    btn.clicked.connect(child_ui.show)


    # btn2 = GuishowChoice_ui.pushButton
    # btn2.clicked.connect(showdialog_ui.show)

    btn3=child_ui.pushButton
    btn3.clicked.connect(GuishowChoice_ui.show)

    # btn4 = showdialog_ui.btn2
    # showdialog_ui.btn2.clicked.connect(MainWin2=MainWindow2())


    btn5 = GuishowChoice_ui.pushButton_6
    btn5.clicked.connect(thread.start)




    btn4=GuishowChoice_ui.pushButton_2
    # btn4.clicked.connect(OpenWeb_ui.run)
    btn4.clicked.connect(MainWin2.show)



    btn6=GuishowChoice_ui.pushButton_7

    btn6.clicked.connect(thread.finished)



    btn7 = GuishowChoice_ui.pushButton

    btn7.clicked.connect(Graph_ui.Get_graph)

    btn8 = GuishowChoice_ui.pushButton_3

    btn8.clicked.connect(Observer_time_report_ui.show)

    btn9 = GuishowChoice_ui.pushButton_4

    btn9.clicked.connect(MyAccess_ui.show)



    #
    # btn9 = Observer_time_report_ui.pushButton
    #
    # btn9.clicked.connect(VisibilityGraphWindow.Get_graph)

    btn10 = Observer_time_report_ui.pushButton_2

    btn10.clicked.connect(VisibilityGraphWindow_ui.Get_graph)





    btn11 = MyAccess_ui.pushButton_2

    btn11.clicked.connect(Access_graph_ui.Get_graph)







    # btn4.clicked.connect()


    # o=child_ui.btn2
    # o.clicked.connect()

    myWin.show()


    sys.exit(app.exec_())