#%--------------------------------------------------------------------------
# %
# % Geodetic: geodetic coordinates (Longitude [rad], latitude [rad],
# %           altitude [m]) from given position vector (r [m])
# %
from Const import Const
from math import sqrt,atan2
def Geodetic(r):

    const=Const()

    R_equ = const['R_Earth']
    f     = const['f_Earth']
    eps=2.22044604925031e-16
    epsRequ = eps*R_equ   #      % Convergence criterion
    e2      = f*(2-f)       # % Square of eccentricity

    X = r[0]                 #% Cartesian coordinates
    Y = r[1]
    Z = r[2]
    rho2 = X*X + Y*Y         #% Square of distance from z-axis

    # % Check validity of input data
    norm_r=sqrt(r.dot(r))
    if norm_r==0:

        print ( ' invalid input in Geodetic constructor\n' )
        lon = 0
        lat = 0
        h   = -const['R_Earth']
        return lon, lat, h


    # % Iteration
    dZ = e2*Z

    while 1:
        ZdZ    = Z + dZ
        Nh     = sqrt ( rho2 + ZdZ*ZdZ )
        SinPhi = ZdZ / Nh  #% Sine of geodetic latitude
        N      = R_equ / sqrt(1-e2*SinPhi*SinPhi)
        dZ_new = N*e2*SinPhi
        if abs(dZ-dZ_new) < epsRequ:

            break

        dZ = dZ_new


    # % Longitude, latitude, altitude
    lon = atan2(Y, X)
    lat = atan2(ZdZ, sqrt(rho2))
    h   = Nh - N

    return lon, lat, h



def test():
    import numpy as np
    r=np.array([3000000.2,5000000.2,7000000.3])
    lon, lat, h=Geodetic(r)

    print(lon, lat, h)



if __name__ == "__main__":

    test()