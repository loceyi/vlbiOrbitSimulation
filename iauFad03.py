
from Const import Const

def iauFad03(t):

    const=Const()

    # % Mean elongation of the Moon from the Sun (IERS Conventions 2003).
    a = ((    1072260.703692 +
            t * ( 1602961601.2090 +
            t * (        - 6.3706 +
            t * (          0.006593 +
            t * (        - 0.00003169 ) ) ) ))%const['TURNAS'] ) * const['DAS2R']

    return a



def test():

    t=1
    a=iauFad03(t)
    print('a',a)




if __name__ == "__main__":

    test()

