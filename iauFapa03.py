



def iauFapa03(t):

    # % General accumulated precession in longitude.
    a = (0.024381750 + 0.00000538691 * t) * t

    return a


def test():

    t=1
    a=iauFapa03(t)
    print('a',a)




if __name__ == "__main__":

    test()