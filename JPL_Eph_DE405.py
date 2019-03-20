import numpy as np
def ephemeris(celestial_body,Julian_date):
    '''

    :param celestial_body:  earthmoon   mercury    pluto   venus
                            jupiter     moon       saturn
                            librations  neptune    sun
                            mars        nutations  uranus
    :param Julian_date:儒略日
    :return:天体的位置（km）,速度（km/day）
    '''
    import de405
    from jplephem import Ephemeris

    eph = Ephemeris(de405)
    position, velocity = eph.position_and_velocity(celestial_body, Julian_date)  # 1980.06.01
    position=np.transpose(position)
    position=np.array(position).flatten()
    velocity=np.transpose(velocity)
    velocity = np.array(velocity).flatten()
    velocity = velocity / 86400
    state=np.array([position,velocity])

    return np.array(state)


def JPL_Eph_DE405(JD):

    '''

    :param JD:
    :return: unit: m type: ndarray  r_Mercury(ECRF), r_Venus(ECRF), r_Earth(ICRF), r_Mars(ECRF),
    r_Jupiter(ECRF), r_Saturn(ECRF), r_Uranus(ECRF), \
    r_Neptune(ECRF), r_Pluto(ECRF), r_Moon(ECRF), r_Sun(ECRF),r_SunSSB(ICRF)
    '''

    Sun_state = ephemeris('sun', JD)  # 太阳星历
    barycenter_statement = ephemeris('earthmoon', JD)

    import de405
    from jplephem import Ephemeris
    eph = Ephemeris(de405)

    Moon_To_Earth_state = ephemeris('moon', JD)  # 本身就是相对地球的


    Earth_state = barycenter_statement - Moon_To_Earth_state * eph.earth_share
    r_Earth = Earth_state[0, :]

    r_Sun = Sun_state[0, :]-r_Earth


    Moon_state = Moon_To_Earth_state

    r_Moon= Moon_state[0, :]

    Mercury_state = ephemeris('mercury', JD)
    r_Mercury=Mercury_state[0,:]-r_Earth

    Venus_state = ephemeris('venus', JD)
    r_Venus = Venus_state[0, :]-r_Earth

    Mars_state = ephemeris('mars', JD)
    r_Mars = Mars_state[0, :]-r_Earth

    Jupiter_state = ephemeris('jupiter', JD)
    r_Jupiter = Jupiter_state[0, :]-r_Earth

    Saturn_state = ephemeris('saturn', JD)
    r_Saturn = Saturn_state[0, :]-r_Earth

    Uranus_state = ephemeris('uranus', JD)
    r_Uranus = Uranus_state[0, :]-r_Earth

    Neptune_state = ephemeris('neptune', JD)
    r_Neptune = Neptune_state[0, :]-r_Earth

    Pluto_state = ephemeris('pluto', JD)
    r_Pluto = Pluto_state[0, :]-r_Earth

    r_SunSSB=Sun_state[0, :]




    #获取的数据是以km为单位，返回值要求为m为单位，需要乘以1e3转化
    return r_Mercury*1e3,r_Venus*1e3,r_Earth*1e3,r_Mars*1e3,r_Jupiter*1e3,r_Saturn*1e3,r_Uranus*1e3, \
           r_Neptune*1e3,r_Pluto*1e3,r_Moon*1e3,r_Sun*1e3,r_SunSSB*1e3









if __name__ == "__main__":

    JD=2457137.4135185187


    r_Mercury, r_Venus, r_Earth, r_Mars, r_Jupiter, r_Saturn, r_Uranus, \
    r_Neptune, r_Pluto, r_Moon, r_Sun,r_SunSSB=JPL_Eph_DE405(JD)


    print('ok')

