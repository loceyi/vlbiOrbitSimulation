
from sklearn.externals import joblib
import numpy as np
from Julian_date import Julian_date
from Visibility_for_Star import Visibility_for_celestial_body
import matplotlib.pyplot as plt

def VGP():

    Direction_Vector=np.array([1,1,1])
    HPOP_Results = joblib.load('data.pkl')
    x = HPOP_Results[1, :]
    y = HPOP_Results[2, :]
    z = HPOP_Results[3, :]
    time = HPOP_Results[0, :]
    position= np.row_stack((x, y))
    position = np.row_stack((position, z))
    Step_Size =10
    Number_Of_Steps=800

    year = 2015
    month = 1
    day = 1
    hour = 0
    minute = 0
    second = 0

    length = Number_Of_Steps  # 设置步长
      # 生成长度为60的数组,要打1.0因为数组数据类型要为float，输入1则默认类型为int
    timeJD = np.arange(0, length, 1)
    Visibility = np.arange(0, length, 1)
    JD_Start=Julian_date(year, month, day, hour, minute, second)

    for i in range(0, length):  # 0~59,没有60

        timeJD[i] = JD_Start+i*Step_Size/86400

        Visibility[i] = Visibility_for_celestial_body(Direction_Vector,position[:,i], timeJD[i])

    plt.plot(time, Visibility)
    plt.show()


def test():

    VGP()
    print('1')



if __name__ == "__main__":

    test()






