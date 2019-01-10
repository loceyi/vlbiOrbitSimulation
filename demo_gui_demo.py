import tkinter as tk
from tkinter import *
from PIL import ImageTk
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
        canvas = Canvas(window, width=600, height=480)
        canvas.pack(expand=YES, fill=BOTH)

        image = ImageTk.PhotoImage(file=r"C:\Users\lenovo\Pictures\Screenshots\4.jpg")
        canvas.create_image(0, 0, image=image, anchor=NW)
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
        tk.Label(window, text='半长轴(千米)：').place(x=30, y=100)
        tk.Label(window, text='偏心率：').place(x=30, y=150)
        tk.Label(window, text='轨道倾角(度)：').place(x=30, y=200)
        tk.Label(window, text='升交点赤经(度)：').place(x=30, y=250)
        tk.Label(window, text='近地点角距(度):').place(x=30, y=300)
        tk.Label(window, text='真近点角(度):').place(x=30, y=350)
        tk.Label(window, text='仿真起始时间：').place(x=300, y=200)
        tk.Label(window, text='年').place(x=440, y=200)
        tk.Label(window, text='月').place(x=490, y=200)
        tk.Label(window, text='日').place(x=530, y=200)
        tk.Label(window, text='仿真结束时间：').place(x=300, y=250)
        tk.Label(window, text='年').place(x=440, y=250)
        tk.Label(window, text='月').place(x=490, y=250)
        tk.Label(window, text='日').place(x=530, y=250)




        var1 = StringVar()
        a=Entry(window, textvariable=var1).place(x=120, y=100)
        var1.set("0")
        semi_major_axis=var1.get()

        var2 = StringVar()
        b=Entry(window, textvariable=var2).place(x=120, y=150)
        var2.set("0")
        Eccentricity = var2.get()



        var3 = StringVar()
        c=Entry(window, textvariable=var3).place(x=120, y=200)
        var3.set("0")
        Inclination = var3.get()



        var4 = StringVar()
        d=Entry(window, textvariable=var4).place(x=120, y=250)
        var4.set("0")
        RAAN = var4.get()






        var5 = StringVar()
        e=Entry(window, textvariable=var5).place(x=120, y=300)
        var5.set("0")
        Perigee = var5.get()




        var6 = StringVar()
        f=Entry(window, textvariable=var6).place(x=120, y=350)
        var6.set("0")
        True_Anomaly = var6.get()




        var7 = StringVar()
        f = Entry(window, textvariable=var7,width=5).place(x=400, y=200)
        var7.set("0")
        Start_time_year = var7.get()

        var8 = StringVar()
        f = Entry(window, textvariable=var8,width=2).place(x=470, y=200)
        var8.set("0")
        Start_time_month = var8.get()

        var9 = StringVar()
        f = Entry(window, textvariable=var9,width=2).place(x=510, y=200)
        var9.set("0")
        Start_time_day = var9.get()





        var10 = StringVar()
        f = Entry(window, textvariable=var10,width=5).place(x=400, y=250)
        var10.set("0")
        Start_time_year = var10.get()

        var11 = StringVar()
        f = Entry(window, textvariable=var11,width=2).place(x=470, y=250)
        var11.set("0")
        Start_time_month = var11.get()

        var12 = StringVar()
        f = Entry(window, textvariable=var12,width=2).place(x=510, y=250)
        var12.set("0")
        Start_time_day = var12.get()



        window.mainloop()


    def refresh(self):
        pass



demo=Demo(1,2)
demo.GUI()

#初始化

# 定义两个函数

# 一个是动画更新