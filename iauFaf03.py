
from Const import Const
def iauFaf03(t):

    const=Const()

    # % Mean longitude of the Moon minus that of the ascending node
    # % (IERS Conventions 2003).
    a = ( (335779.526232 +
            t * ( 1739527262.8478 +
            t * (       - 12.7512 +
            t * (        - 0.001037 +
            t * (          0.00000417 ) ) ) ))%const['TURNAS'] ) * const['DAS2R']

    return a

def test():
    t=1
    a=iauFaf03(t)
    print('a',a)




if __name__ == "__main__":

    test()