
from Const import Const
def iauFae03(t):

    const=Const()

    # % Mean longitude of Earth (IERS Conventions 2003).

    a = ((1.753470314 + 628.3075849991 * t) % const['D2PI'])

    return a


def test():

    t=1
    a=iauFae03(t)
    print('a',a)




if __name__ == "__main__":

    test()