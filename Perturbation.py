# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import odeint
from math import sqrt,cos,pi
from math import radians



def d_earth_nonsphericfigure(orbit_element,t):
    '''
    :param Orbit_Elements: 轨道六根数,单位为弧度
    :param t: 时间
    :return: 微分方程右边的表达式，地球非球型摄动
    '''
    R_earth=6378 #km
    mu=398600 #km^3/s^(-2)
    J2=-1.08264*10**(-3)
    semi_major_axis = orbit_element[0]
    Eccentricity = orbit_element[1]
    Inclination = orbit_element[2]
    RAAN = orbit_element[3]
    Perigee = orbit_element[4]
    True_Anomaly = orbit_element[5]
    p=semi_major_axis**(1-Eccentricity**2)
    n=sqrt(mu/(semi_major_axis)**3)
    d_RAAN=(-2/3)*(R_earth/p)**2*n*J2*cos(Inclination)
    d_Perigee=-3/4*(R_earth/p)**2*n*J2*(1-5*(cos(Inclination)**2))
    return np.array([0, 0, 0,d_RAAN,d_Perigee,n])

def d_lunar_solar(orbit_element,t):
    '''
    :param Orbit_Elements: 轨道六根数,单位为弧度
    :param t: 时间
    :return: 微分方程右边的表达式，日月引力摄动
    '''
    R_earth=6378 #km
    mu=398600 #km^3/s^(-2)
    J2=-1.08264*10**(-3)
    semi_major_axis = orbit_element[0]
    Eccentricity = orbit_element[1]
    Inclination = orbit_element[2]
    RAAN = orbit_element[3]
    Perigee = orbit_element[4]
    True_Anomaly = orbit_element[5]
    p=semi_major_axis**(1-Eccentricity**2)
    n=sqrt(mu/(semi_major_axis)**3)
    d_RAAN=(-2/3)*(R_earth/p)**2*n*J2*cos(Inclination)
    d_Perigee=-3/4*(R_earth/p)**2*n*J2*(1-5*(cos(Inclination)**2))
    return np.array([0, 0, 0,d_RAAN,d_Perigee,n])



t = np.arange(0, 36000, 0.01)
P1 = odeint(d_earth_nonsphericfigure, (7000,0,0,0,0,0),t)  # (0.,1.,0.)是point的初值

def test():
    import pylab as pl
    P1[:, 5] = P1[:, 5] % (2 * pi)
    pl.plot(t, P1[:, 5])
    # pl.show()



if __name__ == "__main__":

    test()





import de405
from jplephem import Ephemeris

eph = Ephemeris(de405)
j=2444391.5
k = eph.position('sun', j)  # 1980.06.01
d=sqrt(k[0]**2+k[1]**2+k[2]**3)
print(d)
# print(k)
# barycenter = eph.position('earthmoon', j)
# moonvector = eph.position('moon', j)
# print(moonvector)
# earth = barycenter - moonvector * eph.earth_share
# moon = barycenter + moonvector * eph.moon_share
# print(earth)
# print(moon)