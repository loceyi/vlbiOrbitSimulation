import numpy as np
from math import pi,floor
from OrbitElementsToRV import orbit_element_to_rv
import Load_data
from scipy import io
from Julian_date import Mjd,Julian_date
from array_compare import intersection



def HPOP():

    #Load basic data
    Cnm, Snm, eopdata, swdata, SOLdata, DTCdata, APdata=Load_data.Load_data()

    mat = io.loadmat('DE436Coeff.mat')

    PC=mat['DE436Coeff']

    #Model parameters

    AuxParam={'Mjd_UTC':0,'area_solar':0,'area_drag':0,'mass':0,'Cr':0,
                  'Cd':0,'n':0,'m':0,'sun':0,'moon':0,'sRad':0,'drag':0,
                  'planets':0,'SolidEarthTides':0,'OceanTides':0,'Relativity':0}

    year=2015
    month=4
    day=24
    hour=21
    minute=55
    second=28.000
    t_start_jd=Julian_date(month,day,year,hour,minute,second)


    orbit_element = np.array([6878, 0.010, 45, 45, 45, 0]) #输入角度单位为度°

    r0,v0 = orbit_element_to_rv(orbit_element)

    Y0=[r0[0],r0[1],r0[2],v0[0],v0[1],v0[2]]

    Mjd_UTC=t_start_jd-2400000.5

    AuxParam['Mjd_UTC'] = Mjd_UTC
    AuxParam['n'] = 40
    AuxParam['m'] = 40
    AuxParam['sun'] = 0
    AuxParam['moon'] = 0
    AuxParam['planets'] = 0
    AuxParam['sRad'] = 0
    AuxParam['drag'] = 1
    AuxParam['SolidEarthTides'] = 0
    AuxParam['OceanTides'] = 0
    AuxParam['Relativity'] = 0
    AuxParam['Cr'] = 1.0
    AuxParam['Cd'] = 4
    AuxParam['mass'] = 8000
    AuxParam['area_drag']=62.5
    AuxParam['area_solar'] = 110.5


    Mjd0 = Mjd_UTC

    Step = 60 #[s]

    N_Step = 10  #26.47hours

    #shorten PC, eopdata, swdata, Cnm, and Snm
    num=int(N_Step*Step/86400)+2
    JD=t_start_jd
    i=np.nonzero((PC[:,0]<=JD))
    j = np.nonzero((PC[:, 1] >= JD))
    i=i[-1]
    i=i[-1]

    PC = PC[i:i + num+1,:]


    mjd=floor(Mjd_UTC)

    i = np.nonzero(mjd==eopdata[3,:])
    i = i[-1]
    i = i[-1]

    eopdata = eopdata[:,i:i + num+1]





    i = np.nonzero(year==swdata[0,:])
    i=i[0]



    j=np.nonzero(month==swdata[1,:])
    j=j[0]

    k=np.nonzero(day==swdata[2,:])
    k=k[0]
    i=i.tolist()
    j=j.tolist()
    k=k.tolist()

    retA = [x for x in i if x in j]
    retB = [x for x in retA if x in k]



    return


def test_HPOP():

    HPOP()


if __name__ == "__main__":

    test_HPOP()

