
from OrbitElementsToRV import orbit_element_to_rv
from numpy import array,sqrt,arccos,pi
from ephemeris_position_ECRF import ephemeris_sun_lunar_ECRF
from math import  degrees

def Visiblity_for_celestial_body (direction_vector,orbit_element,time):
    '''
  
  :param direction_vector: 需要观测天区方向矢量，在ICRF地心坐标系下，严格来说是ECRF
  :param orbit_element: 卫星初始时间的轨道六根数，在ECRF坐标系下
  :param start_time: 需要预测的时间起点
  :param end_time: 预测时间结束点
  :return: 可观测时间段

    '''
    R_earth=6371 #km
    R_sun=6.955*(10**5) #km
    R_moon=3476.28/2  #km
    r,v=orbit_element_to_rv(orbit_element)

    Distance_sat_EarthCenter=sqrt(r.dot(r))

    Position_satellite_ECRF=r

    # 获得太阳和月亮在ECRF下的坐标
    Position_sun_ECRF, Position_moon_ECRF = ephemeris_sun_lunar_ECRF(time)

    #卫星——目标天区矢量和卫星——地心矢量夹角

    x = Position_satellite_ECRF*(-1) #化为指向地心的矢量
    y = direction_vector-Position_satellite_ECRF #卫星指向目标天区的矢量
    # 两个向量
    Lx = sqrt(x.dot(x))
    Ly = sqrt(y.dot(y))
    # 相当于勾股定理，求得斜线的长度
    cos_angle = x.dot(y) / (Lx * Ly)
    # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    angle_arc = arccos(cos_angle)
    angle_degree =degrees(angle_arc)
    # 变为角度




    #判断地球是否挡住了卫星的观测天区
    if angle_degree=





    # 卫星——目标天区矢量和卫星——日心矢量夹角

    x = Position_satellite_ECRF * (-1)  # 化为指向地心的矢量
    y = direction_vector - Position_satellite_ECRF  # 卫星指向目标天区的矢量
    # 两个向量
    Lx = sqrt(x.dot(x))
    Ly = sqrt(y.dot(y))
    # 相当于勾股定理，求得斜线的长度
    cos_angle = x.dot(y) / (Lx * Ly)
    # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    angle_arc = arccos(cos_angle)
    angle_degree = degrees(angle_arc)
    # 变为角度

    # 卫星——目标天区矢量和卫星——月心矢量夹角

    x = Position_satellite_ECRF * (-1)  # 化为指向地心的矢量
    y = direction_vector - Position_satellite_ECRF  # 卫星指向目标天区的矢量
    # 两个向量
    Lx = sqrt(x.dot(x))
    Ly = sqrt(y.dot(y))
    # 相当于勾股定理，求得斜线的长度
    cos_angle = x.dot(y) / (Lx * Ly)
    # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    angle_arc = arccos(cos_angle)
    angle_degree = degrees(angle_arc)
    # 变为角度


















    return 0

def test():

    a=array([7000,0.2,45,20,30,0])
    r,v=orbit_element_to_rv(a)
    print(r,v)



if __name__ == "__main__":

    test()



