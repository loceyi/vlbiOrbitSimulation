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
def AccelHarmonic_ElasticEarth(Mjd_UTC,r_Sun,r_Moon,r,E,UT1_UTC,TT_UTC,x_pole,y_pole):


    const=Const()

    r_ref = 6378.1366e3  # % Earth's radius [m]; ITG-Grace03
    gm = 398600.4415e9  #% [m ^ 3 / s ^ 2];ITG - Grace03

    C=Global_parameters.Cnm
    S=Global_parameters.Snm

    r_Moon = E * r_Moon
    lM, phiM, rM = CalcPolarAngles(r_Moon)
    r_Sun = E * r_Sun
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
        dSnm41 = (-0.00079/5)*( (const.GM_Moon/gm)*((r_ref/rM)^3)*lgM(5,2)*sin(lM)...
               + (const.GM_Sun/gm)*((r_ref/rS)^3)*lgS(5,2)*sin(lS) );
        dCnm42 = (-0.00057/5)*( (const.GM_Moon/gm)*((r_ref/rM)^3)*lgM(5,3)*cos(2*lM)...
               + (const.GM_Sun/gm)*((r_ref/rS)^3)*lgS(5,3)*cos(2*lS) );
        dSnm42 = (-0.00057/5)*( (const.GM_Moon/gm)*((r_ref/rM)^3)*lgM(5,3)*sin(2*lM)...
               + (const.GM_Sun/gm)*((r_ref/rS)^3)*lgS(5,3)*sin(2*lS) );

        % STEP2 CORRECTIONS
        dC20 = 0;
        for i=1:21
            theta_f = -coeff1(i,1:5)*[l lp F D Om]';
            dC20 = dC20 + 1e-12*(coeff1(i,6)*cos(theta_f)-coeff1(i,7)*sin(theta_f));
        end
        dCnm20 = dCnm20 + dC20;

        [year, month, day, hr, min, sec] = invjday(Mjd_UTC+2400000.5);
        [DJMJD0, DATE] = iauCal2jd(year, month, day);
        TIME = (60*(60*hr+min)+sec)/86400;
        UTC = DATE+TIME;
        TT = UTC+TT_UTC/86400;
        TUT = TIME+UT1_UTC/86400;
        UT1 = DATE+TUT;
        theta_g = iauGmst06(DJMJD0, UT1, DJMJD0, TT);
        dC21 = 0;
        dS21 = 0;
        for i=1:48
            theta_f = (theta_g+pi)-coeff0(i,1:5)*[l lp F D Om]';
            dC21 = dC21 + 1e-12*coeff0(i,6)*sin(theta_f);
            dS21 = dS21 + 1e-12*coeff0(i,6)*cos(theta_f);
        end
        dCnm21 = dCnm21 + dC21;
        dSnm21 = dSnm21 + dS21;

        dC22 = 0;
        dS22 = 0;
        for i=1:2
            theta_f = 2*(theta_g+pi)-coeff2(i,1:5)*[l lp F D Om]';
            dC22 = dC22 + 1e-12*coeff2(i,6)*sin(theta_f);
            dS22 = dS22 + 1e-12*coeff2(i,6)*cos(theta_f);
        end
        dCnm22 = dCnm22 + dC22;
        dSnm22 = dSnm22 + dS22;

        % Treatment of the Permanent Tide (elastic Earth)
        dC20 = 4.4228e-8*(-0.31460)*0.29525;
        dCnm20 = dCnm20 - dC20;

        % Effect of Solid Earth Pole Tide (elastic Earth)
        dC21 = -1.290e-9*(x_pole);
        dS21 = 1.290e-9*(y_pole);
        dCnm21 = dCnm21 + dC21;
        dSnm21 = dSnm21 + dS21;

        C(3,1) = C(3,1) + dCnm20;
        C(3,2) = C(3,2) + dCnm21;
        C(3,3) = C(3,3) + dCnm22;
        S(3,2) = S(3,2) + dSnm21;
        S(3,3) = S(3,3) + dSnm22;

        C(4,1) = C(4,1) + dCnm30;
        C(4,2) = C(4,2) + dCnm31;
        C(4,3) = C(4,3) + dCnm32;
        C(4,4) = C(4,4) + dCnm33;
        S(4,2) = S(4,2) + dSnm31;
        S(4,3) = S(4,3) + dSnm32;
        S(4,4) = S(4,4) + dSnm33;

        C(5,1) = C(5,1) + dCnm40;
        C(5,2) = C(5,2) + dCnm41;
        C(5,3) = C(5,3) + dCnm42;
        S(5,2) = S(5,2) + dSnm41;
        S(5,3) = S(5,3) + dSnm42;
    end









    return a









