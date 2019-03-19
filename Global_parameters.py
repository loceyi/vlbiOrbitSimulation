


import Load_data
from scipy import io




Cnm, Snm, eopdata, swdata, SOLdata, DTCdata, APdata=Load_data.Load_data()

mat = io.loadmat('DE436Coeff.mat')

PC=mat['DE436Coeff']

#Model parameters

AuxParam={'Mjd_UTC':0,'area_solar':0,'area_drag':0,'mass':0,'Cr':0,
                  'Cd':0,'n':0,'m':0,'sun':0,'moon':0,'sRad':0,'drag':0,
                  'planets':0,'SolidEarthTides':0,'OceanTides':0,'Relativity':0}




