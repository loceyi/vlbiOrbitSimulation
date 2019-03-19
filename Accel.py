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
def Accel(t,Y,AuxParam):
    '''

    :param t:
    :param Y:
    :param AuxParam: 一定要是字典格式
    :return:
    '''

    

    return np.array(state)


def test_ephemeris():




if __name__ == "__main__":

    test_ephemeris()

