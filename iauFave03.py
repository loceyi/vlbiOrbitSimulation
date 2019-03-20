
from Const import Const
def iauFave03(t):

    const=Const()

    # % Mean longitude of Venus (IERS Conventions 2003)
    a = ((3.176146697 + 1021.3285546211 * t)%const['D2PI'])

    return a



def test():

    t=1
    a=iauFave03(t)
    print('a',a)




if __name__ == "__main__":

    test()