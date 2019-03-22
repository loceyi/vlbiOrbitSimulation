import numpy as np
from math import pi,floor
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
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!不要随意输入整数，最好都用float，int容易溢出
def HPOP():

    #Load basic data

    year=2015
    month=4
    day=24
    hour=21
    minute=55
    second=28.000
    t_start_jd=Julian_date(year,month,day,hour,minute,second)


    orbit_element = np.array([6878, 0.010, 45, 45, 45, 0]) #输入角度单位为度°

    r0,v0 = orbit_element_to_rv(orbit_element)

    Y0=np.array([r0[0]*1e3,r0[1]*1e3,r0[2]*1e3,v0[0]*1e3,v0[1]*1e3,v0[2]*1e3]) #Y0单位为m,m/s

    Mjd_UTC=t_start_jd-2400000.5

    Global_parameters.AuxParam['Mjd_UTC'] = Mjd_UTC
    Global_parameters.AuxParam['n'] = 40
    Global_parameters.AuxParam['m'] = 40
    Global_parameters.AuxParam['sun'] = 1
    Global_parameters.AuxParam['moon'] = 1
    Global_parameters.AuxParam['planets'] = 1
    Global_parameters.AuxParam['sRad'] = 1
    Global_parameters.AuxParam['drag'] = 1
    Global_parameters.AuxParam['SolidEarthTides'] = 0
    Global_parameters.AuxParam['OceanTides'] = 0
    Global_parameters.AuxParam['Relativity'] = 0
    Global_parameters.AuxParam['Cr'] = 1.0
    Global_parameters.AuxParam['Cd'] = 4
    Global_parameters.AuxParam['mass'] = 8000
    Global_parameters.AuxParam['area_drag']=62.5
    Global_parameters.AuxParam['area_solar'] = 110.5



    Mjd0 = Mjd_UTC

    Step = 100 #[s]

    N_Step = 100  #26.47hours

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

    ol = solve_ivp(Accel, [0, N_Step*Step], Y0, method='Radau', t_eval=np.arange(0, N_Step*Step, Step))

    a = ol.y

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    z = a[2,:]

    x = a[1,:]
    y = a[0,:]
    ax.plot(x, y, z, label='parametric curve')
    ax.legend()




    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 5000000 * np.outer(np.cos(u), np.sin(v))
    y = 5000000 * np.outer(np.sin(u), np.sin(v))
    z = 5000000 * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    plt.axis('off')
    ax.plot_surface(x, y, z, rstride=1,  # row 行步长
                    cstride=2,color='w')

    plt.show()

    return


def test_HPOP():

    HPOP()


if __name__ == "__main__":

    test_HPOP()
    print('1')
