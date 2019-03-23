# %--------------------------------------------------------------------------
# %
# % Calculate polar components
# %
# % Last modified:   2018/01/27   M. Mahooti
# %
# %--------------------------------------------------------------------------

from math import sqrt,atan2,pi
import numpy as np

def CalcPolarAngles(m_Vec):

    # % Length of projection in x-y-plane:
    rhoSqr = m_Vec[0] * m_Vec[0] + m_Vec[1] * m_Vec[1]

    # % Norm of vector
    m_r = sqrt(rhoSqr + m_Vec[2] * m_Vec[2])

    # % Azimuth of vector
    if ( (m_Vec[0]==0) and (m_Vec[1]==0) ):

        m_phi = 0

    else:

        m_phi = atan2(m_Vec[1], m_Vec[0])


    if m_phi < 0:

        m_phi = m_phi + 2*pi


    else:

        pass



    # % Altitude of vector

    rho = sqrt( rhoSqr )

    if ( (m_Vec[2]==0) and (rho==0) ):

        m_theta = 0

    else:


        m_theta = atan2(m_Vec[2], rho)




    return m_phi, m_theta, m_r




def test():

    m_Vec=np.array([1.0,2.0,3.0])

    m_phi, m_theta, m_r=CalcPolarAngles(m_Vec)
    print('m_phi, m_theta, m_r',m_phi, m_theta, m_r)



if __name__ == "__main__":

    test()

