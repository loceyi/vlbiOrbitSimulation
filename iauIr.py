#%  - - - - - -
# %   i a u I r
# %  - - - - - -
# %
# %  Initialize an r-matrix to the identity matrix.
# %
# %  This function is part of the International Astronomical Union's
# %  SOFA (Standards Of Fundamental Astronomy) software collection.
# %
# %  Status:  vector/matrix support function.
# %
# %  Returned:
# %     r                 r-matrix
# %
# %  This revision:  2012 April 3
# %
# %  SOFA release 2012-03-01
# %

def iauIr(r):

    r[0,0] = 1.0
    r[0,1] = 0.0
    r[0,2] = 0.0
    r[1,0] = 0.0
    r[1,1] = 1.0
    r[1,2] = 0.0
    r[2,0] = 0.0
    r[2,1] = 0.0
    r[2,2] = 1.0

    return r

def test():
    from numpy import  zeros
    r=zeros([3,3])
    iauIr(r)
    print(r)




if __name__ == "__main__":

    test()