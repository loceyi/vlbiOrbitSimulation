#function = IERS(eop,Mjd_UTC,interp)
from Const import Const
from math import pi,floor
import numpy as np
#!!!!!!!!!!!!!!!!!!!若用*interp，interp是turple，
# 而不是string
def IERS(eop,Mjd_UTC,interp):

    const=Const()

    if (interp =='l'):
        # % linear interpolation
        mjd = (floor(Mjd_UTC))
        i = np.nonzero(mjd == eop[3, :])
        i = i[-1]
        i = i[-1]

        preeop = eop[:, i]

        nexteop = eop[:,i+1]
        mfme = 1440*(Mjd_UTC-floor(Mjd_UTC))
        fixf = mfme/1440
        #% Setting of IERS Earth rotation parameters
        #% (UT1-UTC [s], TAI-UTC [s], x ["], y ["])
        x_pole  = preeop[4]+(nexteop[4]-preeop[4])*fixf
        y_pole  = preeop[5]+(nexteop[5]-preeop[5])*fixf
        UT1_UTC = preeop[6]+(nexteop[6]-preeop[6])*fixf
        LOD     = preeop[7]+(nexteop[7]-preeop[7])*fixf
        dpsi    = preeop[8]+(nexteop[8]-preeop[8])*fixf
        deps    = preeop[9]+(nexteop[9]-preeop[9])*fixf
        dx_pole = preeop[10]+(nexteop[10]-preeop[10])*fixf
        dy_pole = preeop[11]+(nexteop[11]-preeop[11])*fixf
        TAI_UTC = preeop[12]

        x_pole  = x_pole/const['Arcs'] # % Pole coordinate [rad]
        y_pole  = y_pole/const['Arcs']  #% Pole coordinate [rad]
        dpsi    = dpsi/const['Arcs']
        deps    = deps/const['Arcs']
        dx_pole = dx_pole/const['Arcs'] #% Pole coordinate [rad]
        dy_pole = dy_pole/const['Arcs'] #% Pole coordinate [rad]

    else:
        mjd = (floor(Mjd_UTC))

        i = np.nonzero(mjd == eop[3, :])
        i = i[-1]
        i = i[-1]
        eop = eop[:,i]

        #% Setting of IERS Earth rotation parameters
        #% (UT1-UTC [s], TAI-UTC [s], x ["], y ["])
        x_pole  = eop[4]/const['Arcs']  #% Pole coordinate [rad]
        y_pole  = eop[5]/const['Arcs']  #% Pole coordinate [rad]
        UT1_UTC = eop[6]           #% UT1-UTC time difference [s]
        LOD     = eop[7]             #% Length of day [s]
        dpsi    = eop[8]/const['Arcs']
        deps    = eop[9]/const['Arcs']
        dx_pole = eop[10]/const['Arcs'] #% Pole coordinate [rad]
        dy_pole = eop[11]/const['Arcs'] #% Pole coordinate [rad]
        TAI_UTC = eop[12]            #% TAI-UTC time difference [s]






    return x_pole,y_pole,UT1_UTC,LOD,dpsi,deps,dx_pole,dy_pole,TAI_UTC



def test():
    import Load_data
    from scipy import io

    Cnm, Snm, eopdata, swdata, SOLdata, DTCdata, APdata = Load_data.Load_data()
    Mjd_UTC=5.713691351851868e+04
    x_pole, y_pole, UT1_UTC, LOD, dpsi, deps, dx_pole, dy_pole, TAI_UTC=IERS(eopdata, Mjd_UTC,'l')

    print('1')



if __name__ == "__main__":

    test()