import numpy as np
from math import sqrt
# import numpy as np
#
# class MyOrbit:
#     def __init__(self, a):
#         self.local_var_init(a)
#         self.var_a = a
#
#     def local_var_init(self, a):
#         if 2<a<5:
#             self.var_a = a


def rv_to_orbit_element (r,v):
    '''
    :param orbit_element: semi_major_axis, Eccentricity,
           Inclination, RAAN, Perigee, True_Anomaly
           输入时要求半长轴单位为km,其余角度单位为度
    :return: r,velocity

    '''
    mu=398600
    h=np.cross(r,v)
    semi_major_axis=(2/np.abs(r)-(np.abs(v)**2)/mu)
    Eccentricity=sqrt(1-np.abs(h)**2/mu/semi_major_axis)
    c=1-np.abs(r)/semi_major_axis
    eccentric_anomaly=np.arccos(c/Eccentricity)
    true_anomaly=np.arcsin(semi_major_axis*(1-Eccentricity**2)*np.abs(v)/np.abs(h)/Eccentricity)
    Inclination=np.arccos(h[3]/np.abs(h))
    RAAN=np.arctan(h[1]/h[2])
    Perigee=np.arcsin(r[3]/np.abs(r)/np.sin(Inclination))-true_anomaly
    return np.array([semi_major_axis,Eccentricity,Inclination,RAAN,Perigee,eccentric_anomaly])

def test():
    a=np.array([7000,0,0,0,0,360],dtype=float)
    b=rv_to_orbit_element()
    print(b)



if __name__ == "__main__":

    test()
