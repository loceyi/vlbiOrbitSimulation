
#Base on ICRS of IERS,
#input:a,e,i,Omega, omega,E output:

from numpy import mat,cos,sin,array
from math import radians,sqrt,pi
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

    mu=398600 #km^3/s^(-2)
    semi_major_axis=orbit_element[0]
    Eccentricity=orbit_element[1]
    Inclination=radians(orbit_element[2])
    RAAN=radians(orbit_element[3])
    Perigee=radians(orbit_element[4])
    True_Anomaly=radians(orbit_element[5])
    PQ_row_1_1=-sin(RAAN)*cos(Inclination)*sin(Perigee)+cos(RAAN)*cos(Perigee)
    PQ_row_1_2=-sin(RAAN)*cos(Inclination)*cos(Perigee)-cos(RAAN)*sin(Perigee)
    PQ_row_1_3=sin(RAAN) * sin(Inclination)
    PQ_row_2_1= cos(RAAN)*cos(Inclination)*sin(Perigee)+sin(RAAN)*cos(Perigee)
    PQ_row_2_2=cos(RAAN)*cos(Inclination)*cos(Perigee)-sin(RAAN)*sin(Perigee)
    PQ_row_2_3=-cos(RAAN)*sin(Inclination)
    PQ_row_3_1 = sin(Inclination)*sin(Perigee)
    PQ_row_3_2 = sin(Inclination)*cos(Perigee)
    PQ_row_3_3 = cos(Inclination)
    PQ=array([[PQ_row_1_1,PQ_row_1_2,PQ_row_1_3],[PQ_row_2_1,PQ_row_2_2,PQ_row_2_3],[PQ_row_3_1,PQ_row_3_2,PQ_row_3_3]])
    p = semi_major_axis * (1 - Eccentricity ** 2)
    h = sqrt(float(p) * mu)
    r_1= h**2/mu/(1+Eccentricity*cos(True_Anomaly))*array([cos(True_Anomaly),sin(True_Anomaly),0])
    r=PQ.dot(r_1)
    v_1=mu/h*array([-sin(True_Anomaly),Eccentricity+cos(True_Anomaly),0])

    v = PQ.dot(v_1)


    return array([r,v])

def test():

    a=array([7000,0.2,10,10,10,10])
    b=orbit_element_to_rv(a)
    print(b)



if __name__ == "__main__":

    test()
