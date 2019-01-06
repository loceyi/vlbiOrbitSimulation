import numpy as np
def ephemeris_position_ICRF(celestial_body,Julian_date):
    '''

    :param celestial_body:  earthmoon   mercury    pluto   venus
                            jupiter     moon       saturn
                            librations  neptune    sun
                            mars        nutations  uranus
    :param Julian_date:儒略日
    :return:天体的位置（km）,在ICRF下的，以太阳系质心为原点
    '''
    import de405
    from jplephem import Ephemeris

    eph = Ephemeris(de405)
    position= eph.position(celestial_body, Julian_date)  # 1980.06.01
    position=np.transpose(position)
    position=np.array(position).flatten()

    return np.array(position)


def ephemeris_sun_lunar_ECRF(Julian_date):

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

    barycenter_position = ephemeris_position_ICRF('earthmoon', Julian_date)

    import de405
    from jplephem import Ephemeris
    eph = Ephemeris(de405)
    Position_sun = ephemeris_position_ICRF('sun', Julian_date)
    Position_moon_ECRF = ephemeris_position_ICRF('moon', Julian_date)  # 本身就是相对地球的
    Position_earth = barycenter_position - Position_moon_ECRF * eph.earth_share
    Position_sun_ECRF=Position_sun-Position_earth


    return Position_sun_ECRF,Position_moon_ECRF








if __name__ == "__main__":
    Julian_date=2444391.5
    a,b=ephemeris_sun_lunar_ECRF(Julian_date)
    print(a,b)

