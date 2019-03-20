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
def Accel(t,y):
    '''

    :param t:
    :param Y:
    :param AuxParam: 一定要是字典格式
    :return:
    '''

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
    TT = UTC + TT_UTC / 86400
    TUT = TIME + UT1_UTC / 86400
    UT1 = DATE + TUT

    #Polar motion matrix (TIRS->ITRS, IERS 2003)
    Pi = iauPom00(x_pole, y_pole, iauSp00(DJMJD0, TT))

    #Form bias-precession-nutation matrix

    NPB = iauPnm06a(DJMJD0, TT)

    #% Form Earth rotation matrix

    gast = iauGst06(DJMJD0, UT1, DJMJD0, TT, NPB)
    Theta = iauRz(gast, eye(3))










    return


def test():

    Accel()




if __name__ == "__main__":

    test()

