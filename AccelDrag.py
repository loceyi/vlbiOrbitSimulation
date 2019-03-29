#%--------------------------------------------------------------------------
# %
# % AccelDrag: Computes the acceleration due to the atmospheric drag in
# %            ICRF/EME2000 system
# %
# % Inputs:
# %   dens        Atmospheric Density [kg/m^3]
# %   r           Satellite position vector in the inertial system [m]
# %   v           Satellite velocity vector in the inertial system [m/s]
# %   T           Transformation matrix to true-of-date inertial system
# %   Area        Cross-section [m^2]
# %   mass        Spacecraft mass [kg]
# %   CD          Drag coefficient
# %   Omega       Angular velocity of the Earth
# %
# % Output:
# %   a           Acceleration (a=d^2r/dt^2) [m/s^2]
# %
from numpy import cross,transpose,dot
from math import sqrt
def AccelDrag(dens, r, v, T, Area, mass, CD, Omega):
    '''

    :param dens:
    :param r: numpy.array
    :param v: numpy.array
    :param T: numpy.array.matrix
    :param Area:
    :param mass:
    :param CD:
    :param Omega:
    :return:
    '''

    # % Earth angular velocity vector [rad/s]
    omega = transpose([0.0, 0.0, Omega])

    # % Position and velocity in true-of-date system
    r_tod = dot(T,r)
    v_tod = dot(T,v)

    # % Velocity relative to the Earth's atmosphere
    v_rel = v_tod - cross(omega, r_tod)
    v_abs = sqrt(v_rel.dot(v_rel))

    # % Acceleration
    a_tod = -0.5*CD*(Area/mass)*dens*v_abs*v_rel

    a = dot(transpose(T),a_tod)

    return a

def test():
    import numpy as np
    dens=10
    r=np.array([1563234234.8,22342342.8,2342342.8])
    v = np.array([134234.8, 2234.8, 3234.8])
    T=np.array([[134234.8, 2234.8, 3234.8],[123.8,123.8,4352.8],[13.8,324.8,234.8]])
    Area=123123
    mass=1323
    CD=2
    Omega=123

    a=AccelDrag(dens, r, v, T, Area, mass, CD, Omega)

    print(a)



if __name__ == "__main__":

    test()
