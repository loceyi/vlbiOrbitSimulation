


from Const import  Const
def iauFalp03(t):

    const=Const()

    # % Mean anomaly of the Sun (IERS Conventions 2003).
    a = (( 1287104.793048 +
            t * ( 129596581.0481 +
            t * (       - 0.5532 +
            t * (         0.000136 +
            t * (       - 0.00001149 ) ) ) ))% const['TURNAS'] ) * const['DAS2R']

    return a




def test():

    t=1
    a=iauFalp03(t)
    print('a',a)




if __name__ == "__main__":

    test()