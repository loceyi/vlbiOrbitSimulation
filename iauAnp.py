




from Const import Const
def iauAnp(a):

    const=Const()

    w = a%const['D2PI']

    if (w < 0):

        w = w + const['D2PI']


    return w



def test():
    a=1234
    w=iauAnp(a)
    print('w',w)




if __name__ == "__main__":

    test()