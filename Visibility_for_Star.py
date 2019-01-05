
from OrbitElementsToRV import orbit_element_to_rv
from numpy import array
def Visiblity_for_celestial_body (direction_vector,orbit_element,start_time,end_time):
    '''
  
  :param direction_vector: 需要观测天区方向矢量，在ICRF地心坐标系下，严格来说是ECRF
  :param orbit_element: 卫星初始时间的轨道六根数，在ECRF坐标系下
  :param start_time: 需要预测的时间起点
  :param end_time: 预测时间结束点
  :return: 可观测时间段

    '''

    r,v=orbit_element_to_rv(orbit_element)


    #获得太阳和月亮在ECRF下的坐标




    return 0

def test():

    a=array([7000,0.2,45,20,30,0])
    r,v=orbit_element_to_rv(a)
    print(r,v)



if __name__ == "__main__":

    test()


def sun_lunar_position (time):
    '''

    :param time:需求计算的某个时刻
    :return: 太阳和月球在ECRF坐标下的位置

    '''
    from Ephemeris import ephemeris
    import numpy as np
    import de405
    from jplephem import Ephemeris
    Sun_state = ephemeris('sun', time)  # 太阳星历
    barycenter_statement = ephemeris('earthmoon', time)

    eph = Ephemeris(de405)
    Position_sun = Sun_state[0, :]
    Moon_state = ephemeris('moon', time)  # 本身就是相对地球的
    Position_moon = Moon_state[0, :]
    Earth_state = barycenter_statement - Moon_state * eph.earth_share
    Position_earth = Earth_state[0, :]
    Velocity_earth = Earth_state[1, :]

    # 太阳引力摄动

    G = 6.67259 * 10e-11
    M_sun = 1.9885 * 10e30
    R_sun_earth = Position_sun - Position_earth  # 地心ICRF参考系下太阳的位置矢量
    V_sun_earth = Velocity_sun - Velocity_earth  # 地心ICRF参考系下太阳的速度矢量
    r_sun = np.sqrt(R_sun_earth[0] ** 2 + R_sun_earth[1] ** 2 + R_sun_earth[2] ** 2)
    K_sun = G * M_sun / (r_sun ** 3)  # r_sun为日地距

    return sun_postion,moon_position
