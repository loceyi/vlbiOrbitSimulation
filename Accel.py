# %--------------------------------------------------------------------------
# %
# % Accel: Computes the acceleration of an Earth orbiting satellite due to
# %    	 - Earth's harmonic gravity field (including Solid Earth Tides and
# %      	   Ocean Tides),
# %    	 - gravitational perturbations of the Sun, Moon and planets
# %    	 - solar radiation pressure
# %    	 - atmospheric drag and
# %	 	 - relativity
# %
# % Inputs:
# %   Mjd_UTC     Modified Julian Date (UTC)
# %   Y           Satellite state vector in the ICRF/EME2000 system
# %   Area        Cross-section
# %   mass        Spacecraft mass
# %   Cr          Radiation pressure coefficient
# %   Cd          Drag coefficient
# %
# % Output:
# %   dY          Acceleration (a=d^2r/dt^2) in the ICRF/EME2000 system
# %
# % Last modified:   2018/02/11   M. Mahooti
# %
# %--------------------------------------------------------------------------


import Global_parameters
import numpy as np
from IERS import IERS
from timediff import timediff
from invjday import invjday
from iauCal2jd import iauCal2jd
from iauPom00 import iauPom00
from iauSp00 import iauSp00
from iauPnm06a import iauPnm06a
from iauGst06 import iauGst06
from iauRz import iauRz
from Mjday_TDB import Mjday_TDB
from JPL_Eph_DE405 import JPL_Eph_DE405
from AccelPointMass import AccelPointMass
from Const import Const
from AccelSolrad import AccelSolrad
from Relativity import Relativity
from AccelHarmonic_ElasticEarth import AccelHarmonic_ElasticEarth
from JB2008 import JB2008
from AccelDrag import AccelDrag




def Accel(t,Y):
    '''

    :param t:单位是秒
    :param Y:
    :param AuxParam: 一定要是字典格式
    :return:
    '''
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

    # % Difference between ephemeris time and universal time
    # % JD = MJD_UTC+2400000.5;
    # % [year, month, day, hour, minute, sec] = invjday(JD);
    # % days = finddays(year, month, day, hour, minute, sec);
    # % ET_UT = ETminUT(year+days/365.25);
    # % MJD_ET = MJD_UTC+ET_UT/86400;
    # % [r_Mercury,r_Venus,r_Earth,r_Mars,r_Jupiter,r_Saturn,r_Uranus, ...
    # %  r_Neptune,r_Pluto,r_Moon,r_Sun,r_SunSSB] = JPL_Eph_DE436(MJD_ET);
    MJD_TDB = Mjday_TDB(TT)
    JD = MJD_TDB + 2400000.5
    r_Mercury, r_Venus, r_Earth, r_Mars, r_Jupiter, r_Saturn, r_Uranus, \
    r_Neptune, r_Pluto, r_Moon, r_Sun, r_SunSSB = JPL_Eph_DE405(JD)



    # norm_r=np.sqrt(Y[0]**2+Y[1]**2+Y[2]**2)
    # r=Y[0:3]
    # mu=398600*1e9#m^3/s^2
    # a=-mu*r/(norm_r**3)


    a = AccelHarmonic_ElasticEarth(MJD_UTC,r_Sun,r_Moon,Y[0:3],E,UT1_UTC,TT_UTC,x_pole,y_pole)







    if Global_parameters.AuxParam['sun']:

        a = a + AccelPointMass(Y[0:3],r_Sun,const['GM_Sun'])

    if Global_parameters.AuxParam['moon']:

        a = a + AccelPointMass(Y[0:3], r_Moon, const['GM_Moon'])

    if Global_parameters.AuxParam['planets']:

        a = a + AccelPointMass(Y[0:3], r_Mercury, const['GM_Mercury'])
        a = a + AccelPointMass(Y[0:3], r_Venus, const['GM_Venus'])
        a = a + AccelPointMass(Y[0:3], r_Mars, const['GM_Mars'])
        a = a + AccelPointMass(Y[0:3], r_Jupiter, const['GM_Jupiter'])
        a = a + AccelPointMass(Y[0:3], r_Saturn, const['GM_Saturn'])
        a = a + AccelPointMass(Y[0:3], r_Uranus, const['GM_Uranus'])
        a = a + AccelPointMass(Y[0:3], r_Neptune, const['GM_Mercury'])
        a = a + AccelPointMass(Y[0:3], r_Pluto, const['GM_Pluto'])




        #Solar radiation pressure
    if Global_parameters.AuxParam['sRad']:

        a=a+AccelSolrad(Y[0:3],r_Earth,r_Moon,r_Sun,r_SunSSB,
                        Global_parameters.AuxParam['area_solar'],Global_parameters.AuxParam['mass'],
                        Global_parameters.AuxParam['Cr'],const['P_Sol'],const['AU'],'geometrical')



    if Global_parameters.AuxParam['drag']:

           # % Atmospheric density
        # % Omega = 7292115.8553e-11+4.3e-15*( (MJD_UTC-const.MJD_J2000)/36525 ); % [rad/s]
        Omega = const['omega_Earth']-0.843994809*1e-9*LOD #% IERS [rad/s]
        tp,dens = JB2008(MJD_UTC,r_Sun,Y[0:3])
        # % dens = nrlmsise00(MJD_UTC,E*Y(1:3),UT1_UTC,TT_UTC);
        # % [d,~] = msis86(MJD_UTC,E*Y(1:3),gast);
        # % dens = 1e3*d(6);
        # % dens = Density_Jacchia70(r_Sun,MJD_UTC,E*Y(1:3),gast);
        # % dens = Density_HP(r_Sun,NPB*Y(1:3));
        a_Drag =AccelDrag(dens,Y[0:3],Y[3:6],NPB,Global_parameters.AuxParam['area_drag']
                          ,Global_parameters.AuxParam['mass'],Global_parameters.AuxParam['Cd'],Omega)
        a = a + a_Drag




    if Global_parameters.AuxParam['Relativity']:

        a=a+Relativity(Y[0:3],Y[3:6])




    return np.array([Y[3],Y[4], Y[5]
                    ,a[0],a[1],a[2]])


def test():

    Accel()




if __name__ == "__main__":

    test()

