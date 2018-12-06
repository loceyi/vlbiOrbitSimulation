#Base on ICRS of IERS,
#input:a,e,i,Omega, omega,E output:
#角度单位为弧度
from numpy import *
def orbitelementtorv (a,e,i,Omega,omega,f):

    P=mat([[cos(Omega)*cos(omega)-sin(Omega)*sin(omega)*cos(i)],
    [sin(Omega)*cos(omega)+cos(Omega)*sin(omega)*cos(i)],[sin(omega)*sin(i)]])
    Q=mat([[-cos(Omega)*sin(omega)-sin(Omega)*cos(omega)*cos(i)], [sin(Omega)*sin(omega)+cos(Omega)*cos(omega)*cos(i)],
        [cos(omega)*sin(i)]])
    d=a*(1-e*e)/(1+e*cos(f));
    r=d*cos(f)*P+d*sin(f)*Q;

    return r
r=orbitelementtorv(7000,0,0,0,0,0)
print(r)
