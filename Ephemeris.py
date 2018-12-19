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


def test_ephemeris():

    # import Julian_date
    # month = 6
    # day = 1
    # year = 1980
    # hour = 12
    # minute = 0
    # second = 0
    # jd = Julian_date.Julian_date(month, day, year, hour, minute, second)
    # k = ephemeris('moon', jd)#2444391.5
    # print('position=',k[0,:])
    # print('velocity=', k[1, :])

    Sun_state = ephemeris('sun', 2444391.5)  # 太阳星历
    barycenter_statement = ephemeris('earthmoon', 2444391.5)

    import de405
    from jplephem import Ephemeris
    eph = Ephemeris(de405)
    Position_sun = Sun_state[0, :]
    Velocity_sun = Sun_state[1, :]
    Moon_state = ephemeris('moon', 2444391.5)  # 本身就是相对地球的
    Position_moon = Moon_state[0, :]
    Velocity_moon = Moon_state[1, :]
    Earth_state = barycenter_statement - Moon_state * eph.earth_share
    Position_earth = Earth_state[0, :]
    Velocity_earth = Earth_state[1, :]

    R_sun_earth = Position_sun - Position_earth  # 地心ICRF参考系下太阳的位置矢量
    V_sun_earth = Velocity_sun - Velocity_earth  # 地心ICRF参考系下太阳的速度矢量


    print(R_sun_earth,V_sun_earth)


if __name__ == "__main__":

    test_ephemeris()

