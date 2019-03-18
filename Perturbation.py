# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import odeint
from math import sqrt,cos,pi,sin
from math import radians
from Ephemeris import ephemeris
import scipy.integrate as spi
from scipy.integrate import solve_ivp




def pertubation(t,orbit_element):
    '''
    :param Orbit_Elements: 轨道六根数,单位为弧度
    :param t: 时间
    :return: 微分方程右边的表达式
    '''




    '''
    d_earth_nonsphericfigure:地球非球型摄动影响
    '''
    t_start_jd=2458454.0
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
    d_RAAN_earth_nonsphericfigure=(-2/3)*(R_earth/p)**2*n*J2*cos(Inclination)
    d_Perigee_earth_nonsphericfigure=-3/4*(R_earth/p)**2*n*J2*(1-5*(cos(Inclination)**2))
    d_semi_major_axis_earth_nonsphericfigure=0
    d_Eccentricity_earth_nonsphericfigure=0
    d_Inclination_earth_nonsphericfigure=0
    d_Mean_anomaly_earth_nonsphericfigure=0

    '''
    d_lunar_solar日,月引力摄动
    '''
    Sun_state = ephemeris('sun', t_start_jd+t/3600/24)#太阳星历
    barycenter_statement = ephemeris('earthmoon', t_start_jd+t/3600/24)

    import de405
    from jplephem import Ephemeris
    eph = Ephemeris(de405)
    Position_sun=Sun_state[0,:]
    Velocity_sun=Sun_state[1,:]
    Moon_state=ephemeris('moon', t_start_jd+t/3600/24) #本身就是相对地球的
    Position_moon = Moon_state[0, :]
    Velocity_moon = Moon_state[1, :]
    Earth_state = barycenter_statement - Moon_state * eph.earth_share
    Position_earth = Earth_state[0, :]
    Velocity_earth = Earth_state[1, :]

    # 太阳引力摄动

    G=6.67259*10e-11
    M_sun=1.9885*10e30
    R_sun_earth= Position_sun-Position_earth #地心ICRF参考系下太阳的位置矢量
    V_sun_earth= Velocity_sun-Velocity_earth #地心ICRF参考系下太阳的速度矢量
    r_sun=np.sqrt(R_sun_earth[0]**2+R_sun_earth[1]**2+R_sun_earth[2]**2)
    K_sun=G*M_sun/(r_sun**3)#r_sun为日地距

    #计算太阳在地心ICRF坐标系下的轨道根数
    import RV_To_Orbit_Elements
    mu_sun_earth=398600 + G * M_sun / (1e9)  # km^3/s^2
    Sun_Orbit_Elements_ECRF = RV_To_Orbit_Elements.rv_to_orbit_element(R_sun_earth, V_sun_earth,mu_sun_earth)
    Inclination_sun=Sun_Orbit_Elements_ECRF[2]
    RAAN_sun=Sun_Orbit_Elements_ECRF[3]
    Perigee_sun= Sun_Orbit_Elements_ECRF[4]
    True_anomaly_sun=Sun_Orbit_Elements_ECRF[5]
    u_sun=True_anomaly_sun+Perigee_sun
    #计算系数
    A_sun=cos(RAAN-RAAN_sun)*cos(u_sun)+sin(RAAN-RAAN_sun)*sin(u_sun)*cos(Inclination_sun)
    B1_sun=cos(Inclination)
    B2_sun=B1_sun*(-sin(RAAN-RAAN_sun)*cos(u_sun)+sin(u_sun)*cos(Inclination_sun)*cos(RAAN-RAAN_sun))
    B_sun=B2_sun+sin(Inclination)*sin(Inclination_sun)*sin(u_sun)
    C1_sun=sin(Inclination)
    C2_sun=C1_sun*(sin(RAAN-RAAN_sun)*cos(u_sun)-sin(u_sun)*cos(Inclination_sun)*cos(RAAN-RAAN_sun))
    C_sun=C2_sun+cos(Inclination)*sin(Inclination_sun)*sin(u_sun)
    d_semi_major_axis_solar=0
    d_Eccentricity_solar=-(15*K_sun/2/n)*Eccentricity*sqrt(1-Eccentricity**2)* \
                         (A_sun*B_sun*cos(2*Perigee)-(1/2)*(A_sun**2-B_sun**2)*sin(2*Perigee))

    d_Inclination_solar=3*K_sun*C_sun/4/n/sqrt(1-Eccentricity**2)*(A_sun*(2+3*Eccentricity**2+\
                        5*Eccentricity**2*cos(2*Perigee))+5*(B_sun*Eccentricity**2)*sin(2*Perigee))
    d_RAAN_solar = 3*K_sun*C_sun/4/n/sqrt(1-Eccentricity**2)/sin(Inclination)*(B_sun*(2+3*Eccentricity**2+\
                    5*Eccentricity**2*cos(2*Perigee))+5*A_sun*Eccentricity**2*sin(2*Perigee))
    d_Perigee_solar = 3*K_sun/2/n*sqrt(1-Eccentricity**2)*((5*A_sun*B_sun*sin(Perigee*2)+\
                      1/2*(A_sun**2-B_sun**2)*cos(2*Perigee))-1+3/2*(A_sun**2+B_sun**2))\
                      +5*semi_major_axis/2/Eccentricity/r_sun*(1-5/4*(A_sun**2-B_sun**2))*(A_sun*cos(Perigee)\
                      +B_sun*sin(Perigee))-cos(Inclination)*d_RAAN_solar
    d_Mean_anomaly_solar= 0



    # 月球引力摄动


    M_moon=7.349*10e22 #kg
    R_moon_earth= Position_moon #地心ICRF参考系下太阳的位置矢量
    V_moon_earth= Velocity_moon #地心ICRF参考系下太阳的速度矢量
    r_moon=np.sqrt(R_moon_earth.dot(R_moon_earth))
    K_moon=G*M_moon/(r_moon**3)#r_moon为月地距
    mu_moon_earth=398600 + G * M_moon / (1e9)
    #计算月球在地心ICRF坐标系下的轨道根数
    Moon_Orbit_Elements_ECRF = RV_To_Orbit_Elements.rv_to_orbit_element(R_moon_earth, V_moon_earth,mu_moon_earth)
    Inclination_moon=Moon_Orbit_Elements_ECRF[2]
    RAAN_moon=Moon_Orbit_Elements_ECRF[3]
    Perigee_moon= Moon_Orbit_Elements_ECRF[4]
    True_anomaly_moon=Moon_Orbit_Elements_ECRF[5]
    u_moon=True_anomaly_moon+Perigee_moon
    #计算系数
    A_moon=cos(RAAN-RAAN_moon)*cos(u_moon)+sin(RAAN-RAAN_moon)*sin(u_moon)*cos(Inclination_moon)
    B1_moon=cos(Inclination)
    B2_moon=B1_moon*(-sin(RAAN-RAAN_moon)*cos(u_moon)+sin(u_moon)*cos(Inclination_moon)*cos(RAAN-RAAN_moon))
    B_moon=B2_moon+sin(Inclination)*sin(Inclination_moon)*sin(u_moon)
    C1_moon=sin(Inclination)
    C2_moon=C1_moon*(sin(RAAN-RAAN_moon)*cos(u_moon)-sin(u_moon)*cos(Inclination_moon)*cos(RAAN-RAAN_moon))
    C_moon=C2_moon+cos(Inclination)*sin(Inclination_moon)*sin(u_moon)
    d_semi_major_axis_lunar=0
    d_Eccentricity_lunar=-(15*K_moon/2/n)*Eccentricity*sqrt(1-Eccentricity**2)*\
                         (A_moon*B_moon*cos(2*Perigee)-(1/2)*(A_moon**2-B_moon**2)*sin(2*Perigee))

    d_Inclination_lunar=3*K_moon*C_moon/4/n/sqrt(1-Eccentricity**2)*(A_moon*(2+3*Eccentricity**2+\
                        5*Eccentricity**2*cos(2*Perigee))+5*B_moon*Eccentricity**2*sin(2*Perigee))
    d_RAAN_lunar = 3*K_moon*C_moon/4/n/sqrt(1-Eccentricity**2)/sin(Inclination)*(B_moon*(2+3*Eccentricity**2+\
                    5*Eccentricity**2*cos(2*Perigee))+5*A_moon*Eccentricity**2*sin(2*Perigee))
    d_Perigee_lunar = 3*K_moon/2/n*sqrt(1-Eccentricity**2)*((5*A_moon*B_moon*sin(Perigee*2)+\
                      1/2*(A_moon**2-B_moon**2)*cos(2*Perigee))-1+3/2*(A_moon**2+B_moon**2))\
                      +5*semi_major_axis/2/Eccentricity/r_moon*(1-5/4*(A_moon**2-B_moon**2))*(A_moon*cos(Perigee)\
                      +B_moon*sin(Perigee))-cos(Inclination)*d_RAAN_lunar
    d_Mean_anomaly_lunar= 0

    d_semi_major_axis=d_semi_major_axis_earth_nonsphericfigure+d_semi_major_axis_lunar+d_semi_major_axis_solar
    d_Eccentricity = d_Eccentricity_earth_nonsphericfigure+d_Eccentricity_lunar+d_Eccentricity_solar
    d_Inclination=d_Inclination_earth_nonsphericfigure+d_Inclination_solar+d_Inclination_lunar
    d_RAAN=d_RAAN_earth_nonsphericfigure+d_Inclination_lunar+d_RAAN_solar
    d_Perigee=d_Perigee_earth_nonsphericfigure+d_Perigee_lunar+d_Perigee_solar
    d_Mean_anomaly=n


    semi_major_axis_earth_nonsphericfigure=1
    semi_major_axis_lunar_solar=0
    Eccentricity_earth_nonsphericfigure=1
    Eccentricity_lunar_solar=0
    Inclination_earth_nonsphericfigure=1
    Inclination_solar_solar=0
    RAAN_earth_nonsphericfigure=1
    RAAN_lunar_solar=0
    Perigee_earth_nonsphericfigure=1
    Perigee_lunar_solar=0









    return np.array([d_semi_major_axis,d_Eccentricity_earth_nonsphericfigure, d_Inclination_earth_nonsphericfigure
                        ,d_RAAN_earth_nonsphericfigure,d_Perigee_earth_nonsphericfigure,d_Mean_anomaly])




def test_ode_solve():
    # t = np.arange(1, 36000, 1)
    # P1 = odeint(pertubation, (7000,0.5,0.2,0.2,0.2,0.3),t)  # (0.,1.,0.)是point的初值

    orbit_element=[6878,0.010,pi/4,pi/4,pi/4,0]
    t_start = 0
    t_end = 15000
    t_step = 100
    # ode = spi.ode(pertubation,jac=None).set_integrator('vode',nsteps=10000,method='bdf').set_initial_value(orbit_element, t_start)
    #
    # # BDF method suited to stiff systems of ODEs
    #
    #
    #
    # ts = []
    # ys = []
    #
    # while ode.successful() and ode.t < t_end:
    #     print(ode.t + t_step, ode.integrate(ode.t + t_step))
    #     ode.integrate(ode.t + t_step)
    #     ts.append(ode.t)
    #     ys.append(ode.integrate(ode.t+t_step))

    ol = solve_ivp(pertubation, [0, 36000], orbit_element,method='Radau',t_eval= np.arange(0, 36000, 1))
    #P1 = odeint(pertubation, (7000,0 )
    a=ol.y
    import pylab as pl
    ts=np.arange(0, 36000, 1)
    a[5, :] = a[5, :] % (2 * pi)

    pl.figure(1)
    pl.subplot(231)
    pl.plot(ts, a[0, :])


    pl.subplot(232)
    pl.plot(ts, a[1, :])


    pl.subplot(233)
    pl.plot(ts, a[2, :])


    pl.subplot(234)
    pl.plot(ts, a[3, :])


    pl.subplot(235)
    pl.plot(ts, a[4, :])


    pl.subplot(236)
    pl.plot(ts, a[5, :])
    pl.show()



if __name__ == "__main__":

    test_ode_solve()





