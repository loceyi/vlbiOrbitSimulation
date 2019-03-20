



def iauBpn2xy(rbpn):

    # % Extract the X,Y coordinates.
    x = rbpn[2,0]
    y = rbpn[2,1]

    return x, y

def test():
    from numpy import array
    rbpn=array([[1,2,3],[1,2,3],[9,7,3]])
    x, y=iauBpn2xy(rbpn)
    print('x',x,'y',y)




if __name__ == "__main__":

    test()