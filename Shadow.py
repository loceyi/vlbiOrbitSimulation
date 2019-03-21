# %--------------------------------------------------------------------------
# %    Computation of fraction (lambda) of solar disk seen by spacecraft
# %           Beebe, King, Reasonberg, Preston   June 19971
# %
# %                                Vector    Distance
# %        Moon wrt Earth          pccor      rpc
# %        Earth wrt Sun           ccor       rc
# %        Moon wrt Sun            pscor      rps
# %        Satellite wrt Earth     sbcor      rsb
# %        Satellite wrt Sun       bcor       rb
# %        Satellite wrt Moon      sbpcor     rsbp
# %
from Const import Const
import numpy as np
from math import sqrt
from get_lambda import get_lambda

def Shadow(pccor,ccor,pscor,sbcor,bcor,sbpcor):

    const=Const()

    # % shadow computation - geometric model
    # % lambda_1 = 1 - no shadow
    # % lambda_1 = 0 - no sunlight
    # % 0 < lambda_1 < 1 - partial shadow

    # % no consideration is given to the change of direction associated
    # % with partial shadow.
    lambda_1=1
    ecltyp = ''

    # % Check for both eclipses of the Sun by both the Earth and the Moon
    # % First the Earth
    ubcor = np.array([0.0,0.0,0.0])
    rb = np.sqrt(bcor.dot(bcor))
    rc = np.sqrt(ccor.dot(ccor))

    if rb<=rc:

        pass

    else:

        # % get the unit vector of the satellite relative to the sun

        for i in range(1,4):

            ubcor[i-1]=bcor[i-1]/rb



        sepp = np.cross(sbcor,ubcor)

        # % rsbx is the projection of sbcor along bcor
        rsbx = np.dot(sbcor,ubcor)

        # % rs, rp are apparent (from satellite) radii of sun and earth
        # % sep is apparent separation of their centers
        rs=const['R_Sun']/rb
        rp=const['R_Earth']/rsbx
        sep=sqrt(sepp[0]**2+sepp[1]**2+sepp[2]**2)/rsbx

        lambda_1 = get_lambda(rs,rp,sep)

    # % If no Earth eclipse, check the Moon
    if lambda_1<1:

        ecltyp = 'E'

        return lambda_1,ecltyp
    else:

        for i in range(1,4):

            pscor[i-1] = pccor[i-1] + ccor[i-1]
            sbpcor[i-1] = sbcor[i-1] - pccor[i-1]



        rps = sqrt(pscor[0]**2+pscor[1]**2+pscor[2]**2)

        if rb<=rps:

            return lambda_1,ecltyp



        # %   unit vector of SV wrt Sun

        for i in range(1,4):


            ubcor[i-1]=bcor[i-1]/rb




        # % rsbx is the projection of sbcor along bcor
        rsbx=np.dot(sbpcor,ubcor)

        # % rs, rp are apparent (from satellite) radii of sun and moon
        # % sep is apparent angular separation of their centers
        rs=const['R_Sun']/rb
        rp=const['R_Moon']/rsbx

        sepp=np.cross(sbpcor,ubcor)
        sep=sqrt(sepp[0]**2+sepp[1]**2+sepp[2]**2)/rsbx

        lambda_1 = get_lambda(rs,rp,sep)

        if lambda_1<1:

            ecltyp = 'M'



    return lambda_1,ecltyp



def test():
#!!!!!!!!!!!!!!!!!!!!!!!!!若用int容易溢出！！！！！！！！！！！！！！！！！

    pccor=np.array([1234,223,3234.0])
    ccor=np.array([2132.4,3.134,4.45])
    pscor=np.array([2.1324,3.12,4.32])
    sbcor=np.array([4132.4,532.4,6324.4])
    bcor=np.array([4234,56132,713.2])
    sbpcor=np.array([313,423.0,346])


    lambda_1, ecltyp=Shadow(pccor,ccor,pscor,sbcor,bcor,sbpcor)
    print(lambda_1,ecltyp)



if __name__ == "__main__":

    test()