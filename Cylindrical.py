# % Cylindrical: Computes the fractional illumination of a spacecraft in the
# %              vicinity of the Earth assuming a cylindrical shadow model
# %
# % Inputs:
# %   r         Spacecraft position vector [m]
# %   r_Sun     Sun position vector [m]
# %
# % Output:
# %   nu        Illumination factor:
# %             nu=0   Spacecraft in Earth shadow
# %             nu=1   Spacecraft fully illuminated by the Sun
import numpy as np
from Const import Const
def Cylindrical(r, r_Sun):
    '''

    :param r: must be array float
    :param r_Sun: must be array float
    :return:
    '''

    const=Const()
    norm_r_Sun=np.sqrt(r_Sun.dot(r_Sun))
    e_Sun = r_Sun / norm_r_Sun  #% Sun direction unit vector

    s = r.dot(e_Sun)      #% Projection of s/c position

    norm_RSESUN=np.sqrt((r - s * e_Sun).dot(r - s * e_Sun))

    if s>0 or norm_RSESUN>const['R_Earth']:

        nu = 1

    else:

        nu = 0



    return nu




def test():
#!!!!!!!!!!!!!!!!!!!!!!!!!若用int容易溢出！！！！！！！！！！！！！！！！！
    r=np.array([1.0,2.0,3.0])
    r_Sun=np.array([5.0,4.0,5.0])

    nu=Cylindrical(r, r_Sun)
    print(nu)



if __name__ == "__main__":

    test()