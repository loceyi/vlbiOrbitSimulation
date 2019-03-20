#%  - - - - - -
# %   i a u R x
# %  - - - - - -
# %
# %  Rotate an r-matrix about the x-axis.
# %
# %  This function is part of the International Astronomical Union's
# %  SOFA (Standards Of Fundamental Astronomy) software collection.
# %
# %  Status:  vector/matrix support function.
# %
# %  Given:
# %     phi              angle (radians)
# %
# %  Given and returned:
# %     r                r-matrix, rotated
# %
# %  Notes:
# %  1) Calling this function with positive phi incorporates in the
# %     supplied r-matrix r an additional rotation, about the x-axis,
# %     anticlockwise as seen looking towards the origin from positive x.
# %
# %  2) The additional rotation can be represented by this matrix:
# %
# %         (  1        0            0      )
# %         (                               )
# %         (  0   + cos(phi)   + sin(phi)  )
# %         (                               )
# %         (  0   - sin(phi)   + cos(phi)  )
# %
# %  This revision:  2012 April 3
# %
# %  SOFA release 2012-03-01


from math import sin, cos

def iauRx(phi, r):

    s = sin(phi)
    c = cos(phi)

    a10 =   c*r[1,0] + s*r[2,0]
    a11 =   c*r[1,1] + s*r[2,1]
    a12 =   c*r[1,2] + s*r[2,2]
    a20 = - s*r[1,0] + c*r[2,0]
    a21 = - s*r[1,1]+ c*r[2,1]
    a22 = - s*r[1,2] + c*r[2,2]

    r[1,0] = a10
    r[1,1] = a11
    r[1,2] = a12
    r[2,0] = a20
    r[2,1] = a21
    r[2,2] = a22

    return r


def test():
    from math import pi
    import numpy as np
    phi=pi/6
    r=np.array([[0.75,0.433012701892219 ,-0.5],[-0.5,0.866025403784439,0],[0.433012701892219,0.25,0.866025403784439]])
    r=iauRx(phi,r)
    print('r',r)


if __name__ == "__main__":

    test()
