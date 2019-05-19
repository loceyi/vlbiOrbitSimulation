



from sklearn.externals import joblib
from Julian_date import Julian_date
from Ground_Station_Access import GSA
import numpy as np
import matplotlib.pyplot as plt

def GSAT():

    Longitude=45
    Latitude=45
    MAX_ElevationAngle=15
    Altitude =0
    HPOP_Results = joblib.load('data.pkl')
    x = HPOP_Results[1, :]
    y = HPOP_Results[2, :]
    z = HPOP_Results[3, :]
    time = HPOP_Results[0, :]

    # Start_Time = joblib.load('Start_Time.pkl')

    year = 2015
    month = 1
    day = 1
    hour = 0
    minute = 0
    second = 0

    t_start_jd = Julian_date(year, month, day, hour, minute, second)

    MJD_UTC_Start = t_start_jd - 2400000.5


    Visibility_GS_SAT = []
    # np.arange(0, len(time), 1)
    i=0

    for t in time:

        Visibility_GS_SAT.append(GSA(np.array([x[i],y[i],z[i]]),
                                t, Latitude, Longitude, Altitude, MAX_ElevationAngle,MJD_UTC_Start))

        i=i+1

    plt.plot(time, Visibility_GS_SAT)
    plt.show()

def test():

    GSAT()
    print('1')



if __name__ == "__main__":

    test()

