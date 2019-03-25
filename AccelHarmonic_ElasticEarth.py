# % AccelHarmonic: Computes the acceleration due to the harmonic gravity
# %                field of the central body (Solid Earth Tides and Ocean
# %                Tides effects are considered)
# %
# % Inputs:
# %   r_Sun       Geocentric equatorial position (in [m]) referred to the
# %               mean equator and equinox of J2000 (EME2000, ICRF)
# %   r_Moon      Geocentric equatorial position (in [m]) referred to the
# %               mean equator and equinox of J2000 (EME2000, ICRF)
# %   Mjd_UTC     Modified Julian Date of UTC
# %   r           Satellite position vector in the inertial system
# %   E           Transformation matrix to body-fixed system
# %   Cnm,Snm     Spherical harmonics coefficients (normalized)
# %   n_max       Maximum degree
# %   m_max       Maximum order (m_max<=n_max; m_max=0 for zonals, only)
# %   UT1_UTC     UT1-UTC time difference [s]
# %   TT_UTC      TT-UTC time difference [s]
# %   x_pole      X-Pole [rad]
# %   y_pole      Y-Pole [rad]
# %
# % Output:
# %   a           Acceleration (a=d^2r/dt^2)

import Global_parameters
from CalcPolarAngles import CalcPolarAngles
from Const import Const
import numpy as np
from Legendre import Legendre
from math import sin,cos
from invjday import invjday
from iauCal2jd import iauCal2jd
from iauGmst06 import iauGmst06
from math import pi
from math import sqrt,asin,atan2
def AccelHarmonic_ElasticEarth(Mjd_UTC,r_Sun,r_Moon,r,E,UT1_UTC,TT_UTC,x_pole,y_pole):

    '''

    :param Mjd_UTC: float
    :param r_Sun: 行向量
    :param r_Moon: 行向量
    :param r: 行向量
    :param E: 矩阵
    :param UT1_UTC:float
    :param TT_UTC: float
    :param x_pole: float
    :param y_pole: float
    :return: a 行向量
    '''


    const=Const()

    r_ref = 6378.1366e3  # % Earth's radius [m]; ITG-Grace03
    gm = 398600.4415e9  #% [m ^ 3 / s ^ 2];ITG - Grace03

    C=Global_parameters.Cnm
    S=Global_parameters.Snm

    r_Moon = np.dot(E,r_Moon)
    lM, phiM, rM = CalcPolarAngles(r_Moon)
    r_Sun = np.dot(E,r_Sun)
    lS, phiS, rS= CalcPolarAngles(r_Sun)

    Mjd_TT = Mjd_UTC + TT_UTC / 86400

    T = (Mjd_TT - const['MJD_J2000']) / 36525
    T2 = T * T
    T3 = T2 * T
    rev = 360 * 3600 #% arcsec / revolution





    if (Global_parameters.AuxParam['SolidEarthTides']):

        # % Effect of Solid Earth Tides (elastic Earth)
        #     # % For dC21 and dS21
        #     # % The coefficients we choose are in-phase(ip) amplitudes and out-of-phase amplitudes of the
        #     # % corrections for frequency dependence, and multipliers of the Delaunay variables
        #     # % Refer to Table 6.5a in IERS2010
        #%  l   l'  F   D   Om  Amp(R) Amp(I)
        coeff0 = np.array([
           [2,  0,  2,  0,  2,  -0.1,    0],
           [0,  0,  2,  2,  2,  -0.1,    0],
           [1,  0,  2,  0,  1,  -0.1,    0],
           [1,  0,  2,  0,  2,  -0.7,    0.1],
          [-1,  0,  2,  2,  2,  -0.1,    0],
           [0,  0,  2,  0,  1,  -1.3,    0.1],
           [0,  0,  2,  0,  2,  -6.8,    0.6],
           [0,  0,  0,  2,  0,   0.1,    0],
           [1,  0,  2, -2,  2,   0.1,    0],
          [-1,  0,  2,  0,  1,   0.1,    0],
          [-1,  0,  2,  0,  2,   0.4,    0],
           [1,  0,  0,  0,  0,   1.3,   -0.1],
           [1,  0,  0,  0,  1,   0.3,    0],
          [-1,  0,  0,  2,  0,   0.3,    0],
          [-1,  0,  0,  2,  1,   0.1,    0],
           [0,  1,  2, -2,  2,  -1.9,    0.1],
           [0,  0,  2, -2,  1,   0.5,    0],
           [0,  0,  2, -2,  2,  -43.4,   2.9],
           [0, -1,  2, -2,  2,   0.6,    0],
           [0,  1,  0,  0,  0,   1.6,   -0.1],
          [-2,  0,  2,  0,  1,   0.1,    0],
           [0,  0,  0,  0, -2,   0.1,    0],
           [0,  0,  0,  0, -1,  -8.8,    0.5],
           [0,  0,  0,  0,  0,   470.9, -30.2],
           [0,  0,  0,  0,  1,   68.1,  -4.6],
           [0,  0,  0,  0,  2,  -1.6,    0.1],
          [-1,  0,  0,  1,  0,   0.1,    0],
           [0, -1,  0,  0, -1,  -0.1,    0],
           [0, -1,  0,  0,  0,  -20.6,  -0.3],
           [0,  1, -2,  2, -2,   0.3,    0],
           [0, -1,  0,  0,  1,  -0.3,    0],
          [-2,  0,  0,  2,  0,  -0.2,    0],
          [-2,  0,  0,  2,  1,  -0.1,    0],
           [0,  0, -2,  2, -2,  -5.0,    0.3],
           [0,  0, -2,  2, -1,   0.2,    0],
           [0, -1, -2,  2, -2,  -0.2,    0],
           [1,  0,  0, -2,  0,  -0.5,    0],
           [1,  0,  0, -2,  1,  -0.1,    0],
          [-1,  0,  0,  0, -1,   0.1,    0],
          [-1,  0,  0,  0,  0,  -2.1,    0.1],
          [-1,  0,  0,  0,  1,  -0.4,    0],
           [0,  0,  0, -2,  0,  -0.2,    0],
          [-2,  0,  0,  0,  0,  -0.1,    0],
           [0,  0, -2,  0, -2,  -0.6,    0],
           [0,  0, -2,  0, -1,  -0.4,    0],
           [0,  0, -2,  0,  0,  -0.1,    0],
          [-1,  0, -2,  0, -2,  -0.1,    0],
          [-1,  0, -2,  0, -1,  -0.1,    0],
        ])





        # % For dC20
        # % The nominal value k20 for the zonal tides is taken as 0.30190
        # % Refer to Table 6.5b in IERS2010
        #% l   l'  F   D   Om  Amp(R)  Amp(I)
        coeff1 = np.array([

          [0,  0,  0,  0,  1,  16.6,   -6.7],
          [0,  0,  0,  0,  2,  -0.1,    0.1],
          [0, -1,  0,  0,  0,  -1.2,    0.8],
          [0,  0, -2,  2, -2,  -5.5,    4.3],
          [0,  0, -2,  2, -1,   0.1,   -0.1],
          [0, -1, -2,  2, -2,  -0.3,    0.2],
          [1,  0,  0, -2,  0,  -0.3,    0.7],
         [-1,  0,  0,  0, -1,   0.1,   -0.2],
         [-1,  0,  0,  0,  0,  -1.2,    3.7],
         [-1,  0,  0,  0,  1,   0.1,   -0.2],
          [1,  0, -2,  0, -2,   0.1,   -0.2],
          [0,  0,  0, -2,  0,   0.0,    0.6],
         [-2,  0,  0,  0,  0,   0.0,    0.3],
          [0,  0, -2,  0, -2,   0.6,    6.3],
          [0,  0, -2,  0, -1,   0.2,    2.6],
          [0,  0, -2,  0,  0,   0.0,    0.2],
          [1,  0, -2, -2, -2,   0.1,    0.2],
         [-1,  0, -2,  0, -2,   0.4,    1.1],
         [-1,  0, -2,  0, -1,   0.2,    0.5],
          [0,  0, -2, -2, -2,   0.1,    0.2],
         [-2,  0, -2,  0, -2,   0.1,    0.1]
        ])


        # % For dC22 and dS22
        # % Refer to Table 6.5c in IERS2010

        #% l  l' F  D  Om   Amp
        coeff2 = np.array([

          [1, 0, 2, 0, 2,  -0.3],
          [0, 0, 2, 0, 2,  -1.2]
        ])

        # % Mean arguments of luni-solar motion
        # %
        # %   l   mean anomaly of the Moon
        # %   l'  mean anomaly of the Sun
        # %   F   mean argument of latitude
        # %   D   mean longitude elongation of the Moon from the Sun
        # %   Om  mean longitude of the ascending node of the Moon

        l  =  (485866.733 + (1325.0*rev +  715922.633)*T
                                  + 31.310*T2 + 0.064*T3)%rev
        lp =  ( 1287099.804 + (  99.0*rev + 1292581.224)*T
                                  -  0.577*T2 - 0.012*T3)% rev
        F  = (  335778.877 + (1342.0*rev +  295263.137)*T
                                  - 13.257*T2 + 0.011*T3)%rev
        D  = ( 1072261.307 + (1236.0*rev + 1105601.328)*T
                                  -  6.891*T2 + 0.019*T3)% rev
        Om = (  450160.280 - (   5.0*rev +  482890.539)*T
                                  +  7.455*T2 + 0.008*T3)% rev

        # % STEP1 CORRECTIONS
        lgM, dlgM = Legendre(4,4,phiM)
        lgS, dlgS = Legendre(4,4,phiS)
        dCnm20 = (0.29525/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,0] )
        dCnm21 = (0.29470/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,1]*cos(lS) )
        dSnm21 = (0.29470/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,1]*(sin(lM))
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,1]*(sin(lS)) )
        dCnm22 = (0.29801/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,2]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,2]*cos(2*lS) )
        dSnm22 = (0.29801/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,2]*(sin(2*lM))
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,2]*(sin(2*lS)) )
        dCnm30 = (0.093/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,0] )
        dCnm31 = (0.093/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,1]*cos(lS) )
        dSnm31 = (0.093/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,1]*sin(lS) )
        dCnm32 = (0.093/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,2]*cos(2*lS) )
        dSnm32 = (0.093/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,2]*sin(2*lS) )
        dCnm33 = (0.094/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,3]*cos(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,3]*cos(3*lS) )
        dSnm33 = (0.094/7)*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,3]*sin(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,3]*sin(3*lS) )
        dCnm40 = (-0.00087/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[4,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[4,0] )
        dCnm41 = (-0.00079/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[4,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[4,1]*cos(lS) )
        dSnm41 = (-0.00079/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[4,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[4,1]*sin(lS) )
        dCnm42 = (-0.00057/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[4,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[4,2]*cos(2*lS) )
        dSnm42 = (-0.00057/5)*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[4,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[4,2]*sin(2*lS) )

        # % STEP2 CORRECTIONS
        dC20 = 0

        for i in range(1,22):

            theta_f = -coeff1[i-1,0:5].dot(np.array([l,lp,F,D,Om]))
            dC20 = dC20 + 1e-12*(coeff1[i-1,5]*cos(theta_f)-coeff1[i-1,6]*sin(theta_f))


        dCnm20 = dCnm20 + dC20

        year, month, day, hr, min, sec= invjday(Mjd_UTC+2400000.5)
        DJMJD0, DATE = iauCal2jd(year, month, day)
        TIME = (60*(60*hr+min)+sec)/86400
        UTC = DATE+TIME
        TT = UTC+TT_UTC/86400
        TUT = TIME+UT1_UTC/86400
        UT1 = DATE+TUT
        theta_g = iauGmst06(DJMJD0, UT1, DJMJD0, TT)
        dC21 = 0
        dS21 = 0
        for i in range(1,49):

            theta_f = (theta_g+pi)-coeff0[i-1,0:5].dot(np.array([l,lp,F,D,Om]))
            dC21 = dC21 + 1e-12*coeff0[i-1,5]*sin(theta_f)
            dS21 = dS21 + 1e-12*coeff0[i-1,5]*cos(theta_f)

        dCnm21 = dCnm21 + dC21
        dSnm21 = dSnm21 + dS21

        dC22 = 0
        dS22 = 0

        for i in range(1,3):
            theta_f = 2*(theta_g+pi)-coeff2[i-1,0:5].dot(np.array([l,lp,F,D,Om]))
            dC22 = dC22 + 1e-12*coeff2[i-1,5]*sin(theta_f)
            dS22 = dS22 + 1e-12*coeff2[i-1,5]*cos(theta_f)


        dCnm22 = dCnm22 + dC22
        dSnm22 = dSnm22 + dS22

        # % Treatment of the Permanent Tide (elastic Earth)
        dC20 = 4.4228e-8*(-0.31460)*0.29525
        dCnm20 = dCnm20 - dC20

        # % Effect of Solid Earth Pole Tide (elastic Earth)
        dC21 = -1.290e-9*(x_pole)
        dS21 = 1.290e-9*(y_pole)
        dCnm21 = dCnm21 + dC21
        dSnm21 = dSnm21 + dS21

        C[2,0] = C[2,0] + dCnm20
        C[2,1] = C[2,1] + dCnm21
        C[2,2] = C[2,2] + dCnm22
        S[2,1] = S[2,1] + dSnm21
        S[2,2] = S[2,2] + dSnm22

        C[3,0] = C[3,0] + dCnm30
        C[3,1] = C[3,1] + dCnm31
        C[3,2] = C[3,2] + dCnm32
        C[3,3] = C[3,3] + dCnm33
        S[3,1] = S[3,1] + dSnm31
        S[3,2] = S[3,2] + dSnm32
        S[3,3] = S[3,3] + dSnm33

        C[4,0] = C[4,0] + dCnm40
        C[4,1] = C[4,1] + dCnm41
        C[4,2] = C[4,2] + dCnm42
        S[4,1] = S[4,1] + dSnm41
        S[4,2] = S[4,2] + dSnm42



    if Global_parameters.AuxParam['OceanTides']:

        # % Ocean Tides
        lgM, dlgM= Legendre(6,6,phiM)
        lgS, dlgS= Legendre(6,6,phiS)

        dCnm20 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.3075)/5*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,0] )
        dCnm21 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.3075)/5*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,1]*cos(lS) )
        dSnm21 = -0.3075/5*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,1]*sin(lS) )
        dCnm22 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.3075)/5*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,2]*cos(2*lS) )
        dSnm22 = -0.3075/5*( (const['GM_Moon']/gm)*((r_ref/rM)**3)*lgM[2,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**3)*lgS[2,2]*sin(2*lS) )
        dCnm30 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.195)/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,0] )
        dCnm31 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.195)/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,1]*cos(lS) )
        dSnm31 = -0.195/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,1]*sin(lS) )
        dCnm32 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.195)/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,2]*cos(2*lS) )
        dSnm32 = -0.195/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,2]*sin(2*lS) )
        dCnm33 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.195)/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,3]*cos(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,3]*cos(3*lS) )
        dSnm33 = -0.195/7*( (const['GM_Moon']/gm)*((r_ref/rM)**4)*lgM[3,3]*sin(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**4)*lgS[3,3]*sin(3*lS) )
        dCnm40 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.132)/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,0] )
        dCnm41 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.132)/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,1]*cos(lS) )
        dSnm41 = -0.132/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,1]*sin(lS) )
        dCnm42 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.132)/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,2]*cos(2*lS) )
        dSnm42 = -0.132/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,2]*sin(2*lS) )
        dCnm43 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.132)/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,3]*cos(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,3]*cos(3*lS) )
        dSnm43 = -0.132/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,3]*sin(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,3]*sin(3*lS) )
        dCnm44 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.132)/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,4]*cos(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,4]*cos(4*lS) )
        dSnm44 = -0.132/9*( (const['GM_Moon']/gm)*((r_ref/rM)**5)*lgM[4,4]*sin(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**5)*lgS[4,4]*sin(4*lS) )
        dCnm50 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,0] )
        dCnm51 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,1]*cos(lS) )
        dSnm51 = -0.1032/9*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,1]*sin(lS) )
        dCnm52 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,2]*cos(2*lS) )
        dSnm52 = -0.1032/9*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,2]*sin(2*lS) )
        dCnm53 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,3]*cos(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,3]*cos(3*lS) )
        dSnm53 = -0.1032/9*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,3]*sin(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,3]*sin(3*lS) )
        dCnm54 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,4]*cos(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,4]*cos(4*lS) )
        dSnm54 = -0.1032/9*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,4]*sin(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,4]*sin(4*lS) )

        dCnm55 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.1032)/11*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,5]*cos(5*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,5]*cos(5*lS) )

        dSnm55 = -0.1032/9*( (const['GM_Moon']/gm)*((r_ref/rM)**6)*lgM[5,5]*sin(5*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**6)*lgS[5,5]*sin(5*lS) )

        dCnm60 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,0]
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,0] )

        dCnm61 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,1]*cos(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,1]*cos(lS) )
        dSnm61 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,1]*sin(lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,1]*sin(lS) )
        dCnm62 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,2]*cos(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,2]*cos(2*lS) )


        dSnm62 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,2]*sin(2*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,2]*sin(2*lS) )

        dCnm63 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,3]*cos(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,3]*cos(3*lS) )
        dSnm63 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,3]*sin(3*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,3]*sin(3*lS) )
        dCnm64 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,4]*cos(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,4]*cos(4*lS) )
        dSnm64 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,4]*sin(4*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,4]*sin(4*lS) )
        dCnm65 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,5]*cos(5*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,5]*cos(5*lS) )
        dSnm65 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,5]*sin(5*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,5]*sin(5*lS) )
        dCnm66 = 4*pi*r_ref**2*1025/(5.9722e24)*(1-0.0892)/13*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,6]*cos(6*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,6]*cos(6*lS) )
        dSnm66 = -0.0892/9*( (const['GM_Moon']/gm)*((r_ref/rM)**7)*lgM[6,6]*sin(6*lM)
               + (const['GM_Sun']/gm)*((r_ref/rS)**7)*lgS[6,6]*sin(6*lS) )

        C[2,0] = C[2,0] + dCnm20
        C[2,1] = C[2,1] + dCnm21
        C[2,2] = C[2,2] + dCnm22
        S[2,1] = S[2,1] + dSnm21
        S[2,2] = S[2,2] + dSnm22

        C[3,0] = C[3,0] + dCnm30
        C[3,1] = C[3,1] + dCnm31
        C[3,2] = C[3,2] + dCnm32
        C[3,3] = C[3,3] + dCnm33
        S[3,1] = S[3,1] + dSnm31
        S[3,2] = S[3,2] + dSnm32
        S[3,3] = S[3,3] + dSnm33

        C[4,0] = C[4,0] + dCnm40
        C[4,1] = C[4,1] + dCnm41
        C[4,2] = C[4,2] + dCnm42
        C[4,3] = C[4,3] + dCnm43
        C[4,4] = C[4,4] + dCnm44
        S[4,1] = S[4,1] + dSnm41
        S[4,2] = S[4,2] + dSnm42
        S[4,3] = S[4,3] + dSnm43
        S[4,4] = S[4,4] + dSnm44

        C[5,0] = C[5,0] + dCnm50
        C[5,1] = C[5,1] + dCnm51
        C[5,2] = C[5,2] + dCnm52
        C[5,3] = C[5,3] + dCnm53
        C[5,4] = C[5,4] + dCnm54
        C[5,5] = C[5,5] + dCnm55
        S[5,1] = S[5,1] + dSnm51
        S[5,2] = S[5,2] + dSnm52
        S[5,3] = S[5,3] + dSnm53
        S[5,4] = S[5,4] + dSnm54
        S[5,5] = S[5,5] + dSnm55

        C[6,0] = C[6,0] + dCnm60
        C[6,1] = C[6,1] + dCnm61
        C[6,2] = C[6,2] + dCnm62
        C[6,3] = C[6,3] + dCnm63
        C[6,4] = C[6,4] + dCnm64
        C[6,5] = C[6,5] + dCnm65
        C[6,6] = C[6,6] + dCnm66
        S[6,1] = S[6,1] + dSnm61
        S[6,2] = S[6,2] + dSnm62
        S[6,3] = S[6,3] + dSnm63
        S[6,4] = S[6,4] + dSnm64
        S[6,5] = S[6,5] + dSnm65
        S[6,6] = S[6,6] + dSnm66


    # % Body-fixed position
    r_bf = np.dot(E,r)

    # % Auxiliary quantities
    d = sqrt(r_bf.dot(r_bf))                    # distance
    latgc = asin(r_bf[2]/d)
    lon = atan2(r_bf[1],r_bf[0])

    pnm, dpnm = Legendre(Global_parameters.AuxParam['n'],Global_parameters.AuxParam['m'],latgc)

    dUdr = 0
    dUdlatgc = 0
    dUdlon = 0
    q3 = 0
    q2 = q3
    q1 = q2

    for n in range(0,Global_parameters.AuxParam['n']+1):

        b1 = (-gm/(d**2))*((r_ref/d)**n)*(n+1)
        b2 =  (gm/d)*((r_ref/d)**n)
        b3 =  (gm/d)*((r_ref/d)**n)


        for m in range(0,Global_parameters.AuxParam['m']+1):

            q1 = q1 + pnm[n,m]*(C[n,m]*cos(m*lon)+S[n,m]*sin(m*lon))
            q2 = q2 + dpnm[n,m]*(C[n,m]*cos(m*lon)+S[n,m]*sin(m*lon))
            q3 = q3 + m*pnm[n,m]*(S[n,m]*cos(m*lon)-C[n,m]*sin(m*lon))

        dUdr     = dUdr     + q1*b1
        dUdlatgc = dUdlatgc + q2*b2
        dUdlon   = dUdlon   + q3*b3
        q3 = 0
        q2 = q3
        q1 = q2


    # % Body-fixed acceleration
    r2xy = r_bf[0]**2+r_bf[1]**2

    ax = (1/d*dUdr-r_bf[2]/(d**2*sqrt(r2xy))*dUdlatgc)*r_bf[0]-(1/r2xy*dUdlon)*r_bf[1]
    ay = (1/d*dUdr-r_bf[2]/(d**2*sqrt(r2xy))*dUdlatgc)*r_bf[1]+(1/r2xy*dUdlon)*r_bf[0]
    az =  1/d*dUdr*r_bf[2]+sqrt(r2xy)/(d**2)*dUdlatgc

    a_bf = np.array([ax,ay,az])

    # % Inertial acceleration
    a = np.dot(np.transpose(E),np.transpose(a_bf))


    return a


def test():
    from numpy import array
    Mjd_UTC=5000
    r_Sun=array([1,2,3])
    r_Moon=array([2,3,4])
    r=array([2,3,23])
    E=array([[1,23,21.2],[21,213.2,23],[154,543,243.2]])
    UT1_UTC=12
    TT_UTC=12
    x_pole=1.5
    y_pole=2.06
    a=AccelHarmonic_ElasticEarth(Mjd_UTC,r_Sun,r_Moon,r,E,UT1_UTC,TT_UTC,x_pole,y_pole)
    print('a',a)




if __name__ == "__main__":

    test()







