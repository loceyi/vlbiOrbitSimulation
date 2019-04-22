from Const import Const
import Global_parameters
from IERS import IERS
from timediff import timediff
from invjday import invjday
from iauCal2jd import iauCal2jd
from iauPom00 import iauPom00
from iauSp00 import iauSp00
from iauPnm06a import iauPnm06a
from iauGst06 import iauGst06
from iauRz import iauRz
import numpy as np
import pymap3d as pm
from math import degrees
from pylab import *
def get_ground_station_postion_ICRF(t,lat,lon,alt):
    '''

    :param t:相对仿真起始点的时间/s
    :param r_ITRS: 地固坐标系 m
    :return: 地心惯性坐标系 m
    '''


    x, y, z = pm.geodetic2ecef(lat, lon, alt)  #默认为WGS84椭球体
    r_ITRS=np.array([x,y,z])

    const=Const()
    MJD_UTC=Global_parameters.AuxParam['Mjd_UTC']+t/86400
    # JD = MJD_UTC + 2400000.5

    x_pole, y_pole, UT1_UTC, LOD, dpsi, deps, dx_pole, dy_pole, TAI_UTC = IERS(Global_parameters.eopdata
                                                                               , MJD_UTC, 'l')

    UT1_TAI, UTC_GPS, UT1_GPS, TT_UTC, GPS_UTC = timediff(UT1_UTC, TAI_UTC)

    JD = MJD_UTC + 2400000.5

    year, month, day, hour, minute, sec = invjday(JD)

    DJMJD0, DATE = iauCal2jd(year, month, day)

    TIME = (60 * (60 * hour + minute) + sec) / 86400
    UTC = DATE + TIME
    TT = UTC + TT_UTC / 86400   #Terrestrial Time (TT) Terrestrial Time (TT)
                                # used to be known as Terrestrial Dynamical Time (TDT)
    TUT = TIME + UT1_UTC / 86400
    UT1 = DATE + TUT

    #Polar motion matrix (TIRS->ITRS, IERS 2003)
    Pi = iauPom00(x_pole, y_pole, iauSp00(DJMJD0, TT))

    #Form bias-precession-nutation matrix

    NPB = iauPnm06a(DJMJD0, TT)

    #% Form Earth rotation matrix

    gast = iauGst06(DJMJD0, UT1, DJMJD0, TT, NPB)

    Theta = iauRz(gast, np.eye(3))

    #ICRS to ITRS transformation

    E = np.dot(np.dot(Pi, Theta),NPB)

    #ITRS to ICRS transformation

    E_1=np.linalg.inv(E)

    r_ICRF=np.dot(E_1,r_ITRS)

    return r_ICRF


def GSA(r_sat,t,lat,lon,alt,maxElevationAngle):
    '''

    :param r_sat:m
    :param t:s
    :param lat:
    :param lon:
    :param alt:m
    :param maxElevationAngle: /degree
    :return:
    '''

    r_ground_station = get_ground_station_postion_ICRF(t, lat, lon, alt)

    r_GS_To_Sat=r_sat-r_ground_station



    x = r_ground_station  # 化为指向地心的矢量
    y = r_GS_To_Sat # 卫星指向目标天区的矢量
    # 两个向量
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    # 相当于勾股定理，求得斜线的长度
    cos_angle = x.dot(y) / (Lx * Ly)
    # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    angle_arc = np.arccos(cos_angle)
    angle_degree_GroundStation_Sat = degrees(angle_arc)
    # 变为角度
    if angle_degree_GroundStation_Sat> (90-maxElevationAngle):

        Visibility_GS_SAT=0

    else:

        Visibility_GS_SAT = 1

    return Visibility_GS_SAT



def test():
    r_sat=np.array([7000e3,0,0])
    maxElevationAngle=15

    lat=0
    lon=0
    alt=0
    Visibility_GS_SAT =[]
    for t in range(0,86400,100):

        Visibility_GS_SAT.append(GSA(r_sat,t,lat,lon,alt,maxElevationAngle))

    time = np.arange(0, 86400, 100)
    plt.plot(time, Visibility_GS_SAT)
    plt.show()






if __name__ == "__main__":

    test()