# % m         maximum order
# % fi        angle [rad]
# %
# % Outputs:
# % pnm       normalized Legendre polynomial values
# % dpnm      normalized Legendre polynomial first derivative values

from numpy import zeros
from math import sqrt,cos,sin
def Legendre(n,m,fi):

    pnm = zeros([n+1,m+1])
    dpnm = zeros([n+1,m+1])

    pnm[0,0]=1
    dpnm[0,0]=0
    pnm[1,1]=sqrt(3)*cos(fi)
    dpnm[1,1]=-sqrt(3)*sin(fi)
    # % diagonal coefficients

    for i in range(2,n+1):

        pnm[i,i]= sqrt((2*i+1)/(2*i))*cos(fi)*pnm[i-1,i-1]
        dpnm[i,i]= sqrt((2*i+1)/(2*i))*((cos(fi)*dpnm[i-1,i-1])-
                      (sin(fi)*pnm[i-1,i-1]))

    # % horizontal first step coefficients
    for i in range(1,n+1):

        pnm[i,i-1]= sqrt(2*i+1)*sin(fi)*pnm[i-1,i-1]
        dpnm[i,i-1]= sqrt(2*i+1)*((cos(fi)*pnm[i-1,i-1])+(sin(fi)*dpnm[i-1,i-1]))


    # % horizontal second step coefficients
    j=0
    k=2

    while(1):

        for i in range(k,n+1):
            pnm[i,j]=sqrt((2*i+1)/((i-j)*(i+j)))*((sqrt(2*i-1)*sin(fi)*pnm[i-1,j])
                        -(sqrt(((i+j-1)*(i-j-1))/(2*i-3))*pnm[i-2,j]))

            dpnm[i,j]=sqrt((2*i+1)/((i-j)*(i+j)))*((sqrt(2*i-1)*sin(fi)*dpnm[i-1,j])
                    +(sqrt(2*i-1)*cos(fi)*pnm[i-1,j])-(sqrt(((i+j-1)*(i-j-1))/(2*i-3))*dpnm[i-2,j]))

        j = j+1
        k = k+1

        if j>m:

            break




    return pnm, dpnm

def test():

    n=2
    m=3
    fi=1.5

    pnm, dpnm=Legendre(n,m,fi)
    print('pnm' ,pnm,'dpnm', dpnm)



if __name__ == "__main__":

    test()