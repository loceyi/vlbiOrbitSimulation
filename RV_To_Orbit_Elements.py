import numpy as np
import math


def rv_to_orbit_element (R,V):
    '''
    :param orbit_element: semi_major_axis, Eccentricity,
           Inclination, RAAN, Perigee, True_Anomaly
           输入时要求半长轴单位为km,其余角度单位为弧度
    :return: r,velocity

    '''
    mu = 398600
    H_vector = np.cross(R,V)
    h = np.sqrt(H_vector.dot(H_vector))
    r = np.sqrt(R.dot(R))
    v = np.sqrt(V.dot(V))
    vr = (R.dot(V))/r
    Eccentricity_vector = 1/mu*((v**2-mu/r)*R-r*vr*V)
    Eccentricity = np.sqrt(Eccentricity_vector.dot(Eccentricity_vector))
    semi_major_axis = 1/(2/r-(v**2)/mu)
    Inclination = np.arccos(H_vector[2]/h)

    #Calculate the node line N

    N = np.cross([0,0,1],H_vector)
    n = np.sqrt(N.dot(N))
    eps = 1.e-10

    #Calculate the right ascension the ascending node(RAAN)

    if n != 0:  # 判断是否为赤道面平行轨道
        RAAN = np.arccos(N[0]/n)

        if N[1] < 0:

            RAAN = 2*math.pi - RAAN

    else:
        RAAN=0

    #Calculate the argument of perigee

    if n != 0:
        if Eccentricity > eps:

            Perigee = np.arccos((N.dot(Eccentricity_vector))/n/Eccentricity)

            if Eccentricity_vector < 0:

               Perigee = 2*math.pi - Perigee

        else:

            Perigee = 0

    else:

        Perigee = 0

    #Calculate the true anomaly

    if Eccentricity > eps:

        TA = np.arccos((Eccentricity_vector.dot(R))/Eccentricity/r)

        if vr < 0:

            TA = 2*math.pi - TA
    else:

        cp = np.cross(N,R)

        if cp[2] >= 0 :

            TA = np.cos((N.dot(R))/n/r)

        else:

            TA = 2*math.pi - np.cos((N.dot(R))/n/r)


    return np.array([semi_major_axis,Eccentricity,Inclination,RAAN,Perigee,TA])

def test():
    R=np.array([6300,0,0])
    V=np.array([0,7.95,0])
    b=rv_to_orbit_element(R,V)
    print(b)



if __name__ == "__main__":

    test()
