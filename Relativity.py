# #%--------------------------------------------------------------------------
# %
# % Relativisty: Computes the perturbational acceleration due to relativistic
# %              effects
# %
# % Inputs:
# %   r           Satellite position vector
# %   v           Satellite velocity vector
# %
# % Output:
# %   a    		Acceleration (a=d^2r/dt^2)
# #

import  numpy as np
from Const import  Const
def Relativity(r,v):

    const=Const()

    # % Relative position vector of satellite w.r.t. point mass

    r_Sat = np.sqrt(r.dot(r))
    v_Sat = np.sqrt(v.dot(v))

    # % Acceleration
    a = const['GM_Earth']/((const['c_light']**2)*(r_Sat**3))\
        *((4*const['GM_Earth']/r_Sat-v_Sat**2)*r+4*r.dot(v)*v)

    return a


def test():

    r=np.array([1.0,2.0,3.0])
    v=np.array([1,3,5.6])

    a=Relativity(r,v)
    print(a)



if __name__ == "__main__":

    test()