import numpy as np
from math import pi,floor,radians
from OrbitElementsToRV import orbit_element_to_rv
import Load_data
from scipy import io
from Julian_date import Mjd,Julian_date
from array_compare import intersection
from scipy.integrate import solve_ivp
from Accel import  Accel
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Basic_sphere import sat_orbit_plot
import Global_parameters
import pylab as pl
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!不要随意输入整数，最好都用float，int容易溢出
from RV_To_Orbit_Elements import rv_to_orbit_element
from Accel_Two_Body import Accel_Two_Body
from decimal import *
def HPOP():

    #Load basic data

    year=2015
    month=4
    day=24
    hour=21
    minute=55
    second=28.000
    t_start_jd=Julian_date(year,month,day,hour,minute,second)


    orbit_element = np.array([360000.0, 0.4, 45.0, 45.0, 45.0, 0.0]) #输入角度单位为度°

    r0,v0 = orbit_element_to_rv(orbit_element)

    Y0=np.array([r0[0]*1e3,r0[1]*1e3,r0[2]*1e3,v0[0]*1e3,v0[1]*1e3,v0[2]*1e3]) #Y0单位为m,m/s
    orbisgsdfgdf=rv_to_orbit_element(Y0[0:3], Y0[3:6], 398600.4418e9)
    Mjd_UTC=t_start_jd-2400000.5

    Global_parameters.AuxParam['Mjd_UTC'] = Mjd_UTC
    Global_parameters.AuxParam['n'] = 10
    Global_parameters.AuxParam['m'] = 10
    Global_parameters.AuxParam['sun'] = 0
    Global_parameters.AuxParam['moon'] = 0
    Global_parameters.AuxParam['planets'] = 0
    Global_parameters.AuxParam['sRad'] = 0
    Global_parameters.AuxParam['drag'] = 0
    Global_parameters.AuxParam['SolidEarthTides'] = 0
    Global_parameters.AuxParam['OceanTides'] = 0
    Global_parameters.AuxParam['Relativity'] = 0
    Global_parameters.AuxParam['Cr'] = 1.0
    Global_parameters.AuxParam['Cd'] = 4
    Global_parameters.AuxParam['mass'] = 8000
    Global_parameters.AuxParam['area_drag']=62.5
    Global_parameters.AuxParam['area_solar'] = 110.5



    Mjd0 = Mjd_UTC

    Step = 10 #[s]

    N_Step = 800 #26.47hours

    #shorten PC, eopdata, swdata, Cnm, and Snm
    num=int(N_Step*Step/86400)+2
    JD=t_start_jd
    i=np.nonzero((Global_parameters.PC[:,0]<=JD))
    j = np.nonzero((Global_parameters.PC[:, 1] >= JD))
    i=i[-1]
    i=i[-1]

    Global_parameters.PC = Global_parameters.PC[i:i + num+1,:]


    mjd=floor(Mjd_UTC)

    i = np.nonzero(mjd==Global_parameters.eopdata[3,:])
    i = i[-1]
    i = i[-1]

    Global_parameters.eopdata = Global_parameters.eopdata[:,i:i + num+1]





    i = np.nonzero(year==Global_parameters.swdata[0,:])
    i=i[0]



    j=np.nonzero(month==Global_parameters.swdata[1,:])
    j=j[0]

    k=np.nonzero(day==Global_parameters.swdata[2,:])
    k=k[0]
    i=i.tolist()
    j=j.tolist()
    k=k.tolist()

    A = [x for x in i if x in j]
    B = [y for y in A if y in k]
    i=B[0]

    Global_parameters.swdata=Global_parameters.swdata[:,(i-3):(i+num+1)]

    Global_parameters.Cnm = Global_parameters.Cnm[0:Global_parameters.AuxParam['n'] + 1, 0: Global_parameters.AuxParam['n'] + 1]
    Global_parameters.Snm = Global_parameters.Snm[0:Global_parameters.AuxParam['n'] + 1, 0: Global_parameters.AuxParam['n'] + 1]



    #% Ephemeris computation using variable-order Radau IIA integrator with step-size control
    # options = rdpset('RelTol', 1e-13, 'AbsTol', 1e-16);
    # [t, yout] = radau( @ Accel, (0:Step:N_Step * Step), Y0, options);

    # Eph(:, 1) = t;
    # Eph(:, 2: 7) = yout;

    ol = solve_ivp(Accel, [0, N_Step*Step], Y0, method='Radau', t_eval=np.arange(0, N_Step*Step, Step),
                   rtol=1e-3, atol=1e-3)

    a = ol.y



    # # Make data
    # u = np.linspace(0, 2 * np.pi, 100)
    # v = np.linspace(0, np.pi, 100)
    # x = 5000000 * np.outer(np.cos(u), np.sin(v))
    # y = 5000000 * np.outer(np.sin(u), np.sin(v))
    # z = 5000000 * np.outer(np.ones(np.size(u)), np.cos(v))
    #
    # # Plot the surface
    # plt.axis('off')
    # ax.plot_surface(x, y, z, rstride=1,  # row 行步长
    #                 cstride=2, color='w')


    # z = a[2,:]
    # y = a[1,:]
    # x = a[0,:]
    # vx=a[3,:]
    # vy=a[4,:]
    # vz=a[5,:]

    position=a[0:3,:]
    time = ol.t

    # if 0 :
    #
    #     mpl.rcParams['legend.fontsize'] = 10
    #
    #     fig = plt.figure()
    #
    #     ax = fig.gca(projection='3d')
    #     ax.plot(x/1000, y/1000, z/1000, label='parametric curve')
    #     ax.legend()
    #
    #     ax.set_xlim(-6000, 6000)  # 设置横轴范围，会覆盖上面的横坐标,plt.xlim
    #     ax.set_ylim(-6000, 6000)  #
    #     ax.set_zlim(-6000, 6000)
    #     ax.set_xlabel('x')  # 设置x轴名称,plt.xlabel
    #     ax.set_ylabel('y')
    #     ax.set_zlabel('z')
    #     ax.patch.set_alpha(1)
    #     ax.grid(True)
    #     plt.show()



    # if 1:
    #     length=len(x)
    #
    #     orbit_element_data = np.zeros([6,length])
    #
    #     for i in range(1,length+1):
    #
    #         temp=rv_to_orbit_element(np.array([x[i-1],y[i-1],z[i-1]]),
    #                                  np.array([vx[i-1],vy[i-1],vz[i-1]]),398600.4418e9)
    #
    #         orbit_element_data[0,i-1]=temp[0]
    #         orbit_element_data[1, i - 1] =temp[1]
    #         orbit_element_data[2, i - 1] =temp[2]
    #         orbit_element_data[3, i - 1] =temp[3]
    #         orbit_element_data[4, i - 1] =temp[4]
    #         orbit_element_data[5, i - 1] =temp[5]
    #
    #
    #     X=ol.t
    #
    #     pl.figure(1)
    #     pl.subplot(231)
    #     pl.plot(X, orbit_element_data[0,:])
    #     temp=np.array([orbit_element[0]*1e3]*len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('a/m')
    #
    #     pl.subplot(232)
    #     pl.plot(X, orbit_element_data[1,:])
    #     temp = np.array([orbit_element[1]] * len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('e')
    #
    #     pl.subplot(233)
    #     pl.plot(X, orbit_element_data[2,:])
    #     temp = np.array([radians(orbit_element[2])] * len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('i/rad')
    #
    #
    #     pl.subplot(234)
    #     pl.plot(X, orbit_element_data[3,:])
    #     temp = np.array([radians(orbit_element[3])] * len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('RAAN/rad')
    #
    #     pl.subplot(235)
    #     pl.plot(X, orbit_element_data[4,:])
    #     temp = np.array([radians(orbit_element[4])] * len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('Perigee/rad')
    #
    #     pl.subplot(236)
    #     pl.plot(X, orbit_element_data[5,:]% (2 * pi))
    #     temp = np.array([radians(orbit_element[5])] * len(X))
    #     pl.plot(X, temp)
    #     plt.xlabel('t/s')  # 设置x轴名称,plt.xlabel
    #     plt.ylabel('True_anomaly/rad')
    #
    #
    #     pl.show()
    #
    #
    #     # plt.plot(X, orbit_element_data[0,:])
    #     # plt.plot(X, orbit_element_data[1,:])
    #     # plt.plot(X, orbit_element_data[2, :])
    #     # plt.plot(X, orbit_element_data[3, :])
    #     # plt.plot(X, orbit_element_data[4, :])
    #     # plt.plot(X, orbit_element_data[5, :]% (2 * pi))
    #     # 在ipython的交互环境中需要这句话才能显示出来
    #
    #     plt.show()



    return position,time


def test_HPOP():

    position, time=HPOP()

    print('1')


if __name__ == "__main__":

    test_HPOP()
    print('1')
