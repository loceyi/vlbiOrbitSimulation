#
#Base on ICRS of IERS,
#input:a,e,i,Omega, omega,E output:

from numpy import mat,cos,sin,array
from math import radians
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


def orbit_element_to_rv (orbit_element):
    '''
    :param orbit_element: semi_major_axis, Eccentricity,
           Inclination, RAAN, Perigee, True_Anomaly
           输入时要求半长轴单位为km,其余角度单位为度
    :return: r,velocity

    '''
    semi_major_axis=orbit_element[0]
    Eccentricity=orbit_element[1]
    Inclination=radians(orbit_element[2])
    RAAN=radians(orbit_element[3])
    Perigee=radians(orbit_element[4])
    True_Anomaly=radians(orbit_element[5])
    P_row_1=[cos(RAAN) * cos(Perigee) - sin(RAAN) * sin(Perigee) * cos(Inclination)]
    P_row_2=[sin(RAAN) * cos(Perigee) + cos(RAAN) * sin(Perigee) * cos(Inclination)]
    P_row_3=[sin(Perigee) * sin(Inclination)]
    P=mat([P_row_1, P_row_2, P_row_3])
    Q_row_1=[-cos(RAAN) * sin(Perigee) - sin(RAAN) * cos(Perigee) * cos(Inclination)]
    Q_row_2=[sin(RAAN) * sin(Perigee) + cos(RAAN) * cos(Perigee) * cos(Inclination)]
    Q_row_3=[cos(Perigee) * sin(Inclination)]
    Q=mat([ Q_row_1,Q_row_2 ,Q_row_3 ])
    d= semi_major_axis * (1 - Eccentricity * Eccentricity) / (1 + Eccentricity * cos(True_Anomaly))
    r= d * cos(True_Anomaly) * P + d * sin(True_Anomaly) * Q

    return r

def test():
    a=array([7000,0,0,0,0,360],dtype=float)
    b=orbit_element_to_rv(a)
    print(b)



if __name__ == "__main__":
    # r = orbitelementtorv(7000, 0, 0, 0, 0, 0)
    # print(r)
    # l1 = [1,2,3]
    # l2 = list(range(3))
    # l3 = list('456')
    # mtx1 = np.array([l1, l2, l3], dtype=int32);
    # print(mtx1, type(mtx1))
    # print(mtx1 * 3)
    # print(mtx1[1,1:2] * 3 )
    test()
