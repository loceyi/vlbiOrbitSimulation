import numpy as np
from math import pi

def Const():

    const={}

    #Mathematics constants
    const['pi2']=2*pi           #2pi
    const['Rad']=pi/180         #Radians per degree
    const['Deg']=180/pi         #Degrees per radian
    const['Arcs']=3600*180/pi      #Arcseconds per radian

    #General

    const['MJD_J2000']=51544.5      #Modified Julian Date of J2000
    const['T_B1950'] =-0.500002108      #Epoch B1950
    const['c_light'] =299792457.999999984 #Speed of light  [m/s]; DE436
    const['AU'] =149597870699.999988        #Astronomical unit [m]; DE436


    #Physical parameters of the Earth, Sun and Moon

    #Equatorial radius and flattening

    const['R_Earth']=6378.137e3 #Earth's radius [m]; WGS-84
    const['f_Earth'] =1/298.257223563 #Flattening; WGS-84
    const['R_Sun'] =696000e3#Sun's radius [m]; DE436
    const['R_Moon'] =1738e3#Moon's radius [m]; DE436

    #Earth rotation (derivative of GMST at J2000; differs from inertial period by precession)

    const['omega_Earth']=15.04106717866910/3600*const['Rad'] #[rad/s]; WGS-84

    #Gravitational coefficients

    const['GM_Earth']=398600.4418e9  #[m^3/s^2]; WGS-84
    const['GM_Sun'] =132712440041.939377e9#[m^3/s^2]; DE436
    const['GM_Moon'] =4902.800117e9
    const['GM_Mercury'] =22031.780000e9
    const['GM_Venus'] =324858.592000e9
    const['GM_Mars'] =42828.375214e9
    const['GM_Jupiter'] =126712764.133446e9
    const['GM_Saturn'] =37940585.200000e9
    const['GM_Uranus'] =5794556.465752e9
    const['GM_Neptune'] =6836527.100580e9
    const['GM_Pluto'] =975.501176e9


    #Solar radiation pressure at 1 AU

    const['P_Sol']=1367/const['c_light'] #[N/m^2] (1367 W/m^2); IERS


    #Arcseconds to radians

    const['AS2R']=4.848136811095359935899141e-6

    #Pi

    const['DPI'] = 3.141592653589793238462643

    #2Pi

    const['D2PI'] = 6.283185307179586476925287

    #Degrees to radians

    const['DD2R'] = 1.745329251994329576923691e-2

    #Radians to arcseconds

    const['DR2AS'] = 206264.8062470963551564734

    #Arcseconds to radians

    const['DAS2R'] = 4.848136811095359935899141e-6

    #Seconds of time to radians

    const['DS2R'] = 7.272205216643039903848712e-5

    #Arcseconds in a full circle

    const['TURNAS'] = 1296000.0

    #Milliarcseconds to radians

    const['DMAS2R'] = const['DAS2R']/(1e3)

    #Length of tropical year B1900 (days)

    const['DTY'] = 365.242198781

    #seconds per day.

    const['DAYSEC'] = 86400.0

    #Days per Julian year

    const['DJY'] = 365.25

    #Days per Julian century

    const['DJC'] = 36525.0

    #Days per Julian millennium

    const['DJM'] = 365250.0

    #Reference epoch (J2000.0), Julian Date

    const['DJ00'] = 2451545.0

    #Julian Date of Modified Julian Date zero

    const['DJM0'] = 2400000.5

    #Reference epoch (J2000.0), Modified Julian Date

    const['DJM00'] = 51544.5

    #1977 Jan 1.0 as MJD

    const['DJM77'] = 43144.0

    #TT minus TAI (s)

    const['TTMTAI'] = 32.184

    #Astronomical unit [m]; DE405;

    const['DAU'] = 149597870691.000015

    #Speed of light (m/s)

    const['CMPS'] = 299792458.0

    #Light time for 1 au (s)

    const['AULT'] = 499.004782

    #Speed of light (AU per day)

    const['DC'] = const['DAYSEC'] / 499.004782

    #L_G = 1 - d(TT)/d(TCG)

    const['ELG'] = 6.969290134e-10

    #L_B = 1 - d(TDB)/d(TCB), and TDB (s) at TAI 1977/1/1.0

    const['ELB'] = 1.550519768e-8
    const['TDB0'] = -6.55e-5

    #Schwarzschild radius of the Sun (au)= 2 * 1.32712440041e20 / (2.99792458e8)^2 / 1.49597870700e11

    const['SRS'] = 1.97412574336e-8






    return const


def test_Const():

    const=Const()
    print(const)




if __name__ == "__main__":

    test_Const()

