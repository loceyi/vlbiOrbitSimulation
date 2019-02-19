from Visibility_for_Star import *
from Julian_date import Julian_date
import numpy
import matplotlib.pyplot as plt
from pylab import *


import matplotlib as mpl
import matplotlib.pyplot as plt

#from 2019年1月15日9：00到12:00
month = 3
day = 15
year = 2017
hour = 9
minute = 0
second = 0
length=60#设置步长
time=np.arange(0,length,1.0)#生成长度为60的数组,要打1.0因为数组数据类型要为float，输入1则默认类型为int
Visibility=np.arange(0,length,1)
for i in range(0,length): #0~59,没有60


    minute=i+1
    time[i] = Julian_date(month, day, year, hour, minute, second)

    a = array([7000, 0.2, 45, 20, 30, 0])
    direction_vector = array([1, 1, 0.1])
    Visibility[i] = Visibility_for_celestial_body(direction_vector, a, time[i])



#xlim(time[0,1], time[0,10])
#设置y轴范围
#ylim(0, 2)
#Visibility=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

plt.plot(time, Visibility)
plt.show()

















