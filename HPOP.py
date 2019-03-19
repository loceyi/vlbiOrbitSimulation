import numpy as np
def HPOP():


    Cnm=np.zeros([181,181])
    Snm = np.zeros([181, 181])
    with open('GGM03S.txt','r') as f:


        line=f.readline()


        for n in range(0,181):

            for m in range(0,n+1):

                temp = list(map(float, line.split()))

                Cnm[n, m] = temp[2]
                Snm[n, m] = temp[3]

                line = f.readline()




























    return


def test_HPOP():

    HPOP()


if __name__ == "__main__":

    test_HPOP()

