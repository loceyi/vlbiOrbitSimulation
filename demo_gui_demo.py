import tkinter as tk
from tkinter import Menu
import pygame
import RV_To_Orbit_Elements


class Demo:
    pass
    def __init__(self,R,V):
        self.R=R
        self.V=V


    def GUI(self):
        def hello():
            print("hello!")

        window = tk.Tk()
        window.title('Orbit Demo')
        window.wm_geometry('600x480+300+100')
        # 创建菜单栏功能
        menuBar = Menu(window)
        window.config(menu=menuBar)
        # 创建一个名为File的菜单项
        fileMenu = Menu(menuBar,tearoff=0)
        menuBar.add_cascade(label="选项", menu=fileMenu)

        # 在菜单项File下面添加一个名为New的选项
        fileMenu.add_command(label="运行")

        helpMenu = Menu(menuBar, tearoff=0)
        # 在菜单栏中创建一个名为Help的菜单项helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="帮助", menu=helpMenu)
        # 在菜单栏Help下添加一个名为About的选项
        helpMenu.add_command(label="关于")

        tk.Label(window, text='请输入初始轨道六根数').place(x=240, y=30)
        tk.Label(window, text='半长轴：').place(x=30, y=100)
        tk.Label(window, text='偏心率：').place(x=30, y=150)
        tk.Label(window, text='轨道倾角：').place(x=30, y=200)
        tk.Label(window, text='升交点赤经：').place(x=30, y=250)
        tk.Label(window, text='近地点角距:').place(x=30, y=300)
        tk.Label(window, text='真近点角:').place(x=30, y=350)



        window.mainloop()


    def refresh(self):
        pass



demo=Demo(1,2)
demo.GUI()

#初始化

# 定义两个函数

# 一个是动画更新