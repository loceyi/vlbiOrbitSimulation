
from Const import Const
def iauFal03(t):

    const=Const()

    # % Mean anomaly of the Moon (IERS Conventions 2003).
    a = ( (485868.249036 +
            t * ( 1717915923.2178 +
            t * (         31.8792 +
            t * (          0.051635 +
            t * (        - 0.00024470 ) ) ) ))% const['TURNAS'] ) * const['DAS2R']

    return a

def test():
    t=1
    a=iauFal03(t)
    print('a',a)




if __name__ == "__main__":

    test()