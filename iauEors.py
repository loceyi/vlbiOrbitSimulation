
from math import atan2

def iauEors(rnpb, s):

    # % Evaluate Wallace & Capitaine (2006) expression (16).
    x = rnpb[2,0]
    ax = x / (1 + rnpb[2,2])
    xs = 1 - ax * x
    ys = -ax * rnpb[2,1]
    zs = -x
    p = rnpb[0,0] * xs + rnpb[0,1] * ys + rnpb[0,2] * zs
    q = rnpb[1,0] * xs + rnpb[1,1] * ys + rnpb[1,2] * zs

    if (p != 0) or (q != 0):

        eo = s - atan2(q, p)

    else:

        eo = s



    return eo



def test():
    from numpy import array
    rnpb=array([[1,2,3],[4,5,6],[7,8,9]])
    s=1
    eo=iauEors(rnpb, s)
    print('eo',eo)




if __name__ == "__main__":

    test()