# #%--------------------------------------------------------------------------
# %
# % AccelPointMass: Computes the perturbational acceleration due to a point
# %				  mass
# %
# % Inputs:
# %   r           Satellite position vector
# %   s           Point mass position vector
# %   GM          Gravitational coefficient of point mass
# %
# % Output:
# %   a    		Acceleration (a=d^2r/dt^2)
import numpy as np

def AccelPointMass(r, s, GM):
    '''

    :param r: 必须为一维array，不能有换行号,且数据类型要为float
    :param s: 必须为一维array，不能有换行号,且数据类型要为float
    :param GM:
    :return: a array([x y x])
    '''

    # % Relative position vector of satellite w.r.t. point mass
    d = r - s

    # % Acceleration
    norm_d=np.sqrt(d.dot(d))
    norm_s=np.sqrt(s.dot(s))
    a = -GM * ( d/(norm_d**3) + s/(norm_s**3) )



    return a

def test():

    r=np.array([1.0,2.0,3.0])
    s=np.array([5.0,4.0,5.0])
    GM=100
    a=AccelPointMass(r, s, GM)
    print(a)



if __name__ == "__main__":

    test()