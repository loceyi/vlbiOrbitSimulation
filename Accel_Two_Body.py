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



import numpy as np
from Const import Const





def Accel_Two_Body(t,Y):
    '''
    :param t:
    :param Y:
    :return:
    '''


    norm_r = np.sqrt(Y[0] ** 2 + Y[1] ** 2 + Y[2] ** 2)
    r = Y[0:3]
    mu = 398600 * 1e9  # m^3/s^2
    a = -mu * r / (norm_r ** 3)








    return np.array([Y[3],Y[4], Y[5]
                ,a[0],a[1],a[2]])


def test():

    Accel_Two_Body()




if __name__ == "__main__":

    test()

