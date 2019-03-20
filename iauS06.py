# #%   - - - - - - -
# %    i a u S 0 6
# %   - - - - - - -
# %
# %   The CIO locator s, positioning the Celestial Intermediate Origin on
# %   the equator of the Celestial Intermediate Pole, given the CIP's X,Y
# %   coordinates.  Compatible with IAU 2006/2000A precession-nutation.
# %
# %   This function is part of the International Astronomical Union's
# %   SOFA (Standards Of Fundamental Astronomy) software collection.
# %
# %   Status:  canonical model.
# %
# %   Given:
# %      date1,date2       TT as a 2-part Julian Date (Note 1)
# %      x,y               CIP coordinates (Note 3)
# %
# %   Returned (function value):
# %                        the CIO locator s in radians (Note 2)
# %
# %   Notes:
# %
# %   1) The TT date date1+date2 is a Julian Date, apportioned in any
# %      convenient way between the two arguments.  For example,
# %      JD(TT)=2450123.7 could be expressed in any of these ways,
# %      among others:
# %
# %             date1          date2
# %
# %          2450123.7           0.0       (JD method)
# %          2451545.0       -1421.3       (J2000 method)
# %          2400000.5       50123.2       (MJD method)
# %          2450123.5           0.2       (date & time method)
# %
# %      The JD method is the most natural and convenient to use in
# %      cases where the loss of several decimal digits of resolution
# %      is acceptable.  The J2000 method is best matched to the way
# %      the argument is handled internally and will deliver the
# %      optimum resolution.  The MJD method and the date & time methods
# %      are both good compromises between resolution and convenience.
# %
# %   2) The CIO locator s is the difference between the right ascensions
# %      of the same point in two systems:  the two systems are the GCRS
# %      and the CIP,CIO, and the point is the ascending node of the
# %      CIP equator.  The quantity s remains below 0.1 arcsecond
# %      throughout 1900-2100.
# %
# %   3) The series used to compute s is in fact for s+XY/2, where X and Y
# %      are the x and y components of the CIP unit vector;  this series
# %      is more compact than a direct series for s would be.  This
# %      function requires X,Y to be supplied by the caller, who is
# %      responsible for providing values that are consistent with the
# %      supplied date.
# %
# %   4) The model is consistent with the "P03" precession (Capitaine et
# %      al. 2003), adopted by IAU 2006 Resolution 1, 2006, and the
# %      IAU 2000A nutation (with P03 adjustments).
# %
# %   Called:
# %      iauFal03     mean anomaly of the Moon
# %      iauFalp03    mean anomaly of the Sun
# %      iauFaf03     mean argument of the latitude of the Moon
# %      iauFad03     mean elongation of the Moon from the Sun
# %      iauFaom03    mean longitude of the Moon's ascending node
# %      iauFave03    mean longitude of Venus
# %      iauFae03     mean longitude of Earth
# %      iauFapa03    general accumulated precession in longitude
# %
# %   References:
# %      Capitaine, N., Wallace, P.T. & Chapront, J., 2003, Astron.
# %      Astrophys. 432, 355
# %
# %      McCarthy, D.D., Petit, G. (eds.) 2004, IERS Conventions (2003),
# %      IERS Technical Note No. 32, BKG
# %
# %   This revision:  2009 December 17
# %
# %   SOFA release 2012-03-01
# %
from scipy import io
from numpy import shape
from Const import Const
from iauFal03 import iauFal03
from iauFlap03 import iauFalp03
from iauFaf03 import iauFaf03
from iauFad03 import iauFad03
from iauFaom03 import iauFaom03
from iauFave03 import iauFave03
from iauFae03 import iauFae03
from iauFapa03 import iauFapa03
from math import sin, cos
#!!!!!!!!!!!!!!!!!!!!!!!!从mat取出来的一维数组位置index也需要两个
def iauS06(date1, date2, x, y):

        #% ---------------------
    # % The series for s+XY/2
    # % ---------------------
    #
    # % Polynomial coefficients: 1-6
    const=Const()
    mat = io.loadmat('sp.mat')

    sp=mat['sp']

    #%  Terms of order t^0
    mat = io.loadmat('s0.mat')

    s0 = mat['s0']

    #Terms of order t^1
    mat = io.loadmat('s1.mat')

    s1 = mat['s1']

    #Terms of order t^2
    mat = io.loadmat('s2.mat')

    s2 = mat['s2']

    #Terms of order t^3

    mat = io.loadmat('s3.mat')

    s3 = mat['s3']

    #Terms of order t^4
    mat = io.loadmat('s4.mat')

    s4 = mat['s4']


    # %  Number of terms in the luni-solar nutation model
    temporary_parameter = shape(s0)
    NS0=temporary_parameter[0]
    temporary_parameter = shape(s1)
    NS1 = temporary_parameter[0]
    temporary_parameter = shape(s2)
    NS2 = temporary_parameter[0]
    temporary_parameter = shape(s3)
    NS3 = temporary_parameter[0]
    temporary_parameter = shape(s4)
    NS4 = temporary_parameter[0]



    #% Interval between fundamental epoch J2000.0 and current date (JC).
    t = ((date1 - const['DJ00']) + date2) / const['DJC']

    # % Fundamental Arguments (from IERS Conventions 2003)

    # % Mean anomaly of the Moon.
    fa_1 = iauFal03(t)

    # % Mean anomaly of the Sun.
    fa_2 = iauFalp03(t)

    # % Mean longitude of the Moon minus that of the ascending node.
    fa_3 = iauFaf03(t)

    # % Mean elongation of the Moon from the Sun.
    fa_4 = iauFad03(t)

    # % Mean longitude of the ascending node of the Moon.
    fa_5 = iauFaom03(t)

    # % Mean longitude of Venus.
    fa_6 = iauFave03(t)

    # % Mean longitude of Earth.
    fa_7 = iauFae03(t)

    # % General precession in longitude.
    fa_8 = iauFapa03(t)


    fa=[fa_1,fa_2,fa_3,fa_4,fa_5,fa_6,fa_7,fa_8]


    # % Evaluate s.
    w0 = sp[0,0]
    w1 = sp[0,1]
    w2 = sp[0,2]
    w3 = sp[0,3]
    w4 = sp[0,4]
    w5 = sp[0,5]

    for i in range(NS0,0,-1):
        a = 0

        for j in range(1,9):

            a = a + s0[i-1,j-1] * fa[j-1]




        w0 = w0 + s0[i-1,8] * sin(a) + s0[i-1,9] * cos(a)


    for i in range(NS1,0,-1):

        a = 0

        for j in range(1,9):

            a = a + s1[i-1,j-1] * fa[j-1]

        w1 = w1 + s1[i-1,8] * sin(a) + s1[i-1,9] * cos(a)


    for i in range(NS2,0,-1):


        a = 0
        for j in range(1,9):

            a = a + s2[i-1,j-1] * fa[j-1]

        w2 = w2 + s2[i-1,8] * sin(a) + s2[i-1,9] * cos(a)



    for i in range(NS3,0,-1):

        a = 0

        for j in range(1,9):

            a = a + s3[i-1,j-1] * fa[j-1]

        w3 = w3 + s3[i-1,8] * sin(a) + s3[i-1,9] * cos(a)


    for i in range(NS4,0,-1):
        a = 0
        for j in range(1,9):

            a = a + s4[i-1,j-1] * fa[j-1]

        w4 = w4 + s4[i-1,8] * sin(a) + s4[i-1,9] * cos(a)


    s = (w0 + (w1 + (w2 + (w3 + (w4 + w5 * t) * t) * t) * t) * t) * const['DAS2R'] - x*y/2.0




    return s


def test():
    date1=2450123.7
    date2=0
    x=1
    y=0
    s=iauS06(date1, date2, x, y)
    print('s',s)




if __name__ == "__main__":

    test()