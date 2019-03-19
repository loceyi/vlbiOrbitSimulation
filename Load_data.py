import numpy as np


def Load_data():
    Cnm = np.zeros([181, 181])
    Snm = np.zeros([181, 181])

    with open('GGM03S.txt', 'r') as f:

        line = f.readline()

        for n in range(0, 181):

            for m in range(0, n + 1):
                temp = list(map(float, line.split()))

                Cnm[n, m] = temp[2]
                Snm[n, m] = temp[3]

                line = f.readline()

    with open('eop19990101.txt', 'r') as eop:

        eopdata_str = eop.readlines()

    eopdata = np.zeros([13, 7124])
    i = 0

    for eopdata_elements in eopdata_str:
        eopdata[:, i] = list(map(float, eopdata_elements.split()))
        i = i + 1

    with open('sw19990101.txt', 'r') as sw:

        sw_str = sw.readlines()

    swdata = np.zeros([33, 6909])
    i = 0

    for sw_elements in sw_str:
        swdata[:, i] = list(map(float, sw_elements.split()))
        i = i + 1

    with open('SOLFSMY.txt', 'r') as SOL:

        SOL_str = SOL.readlines()

    SOLdata = np.zeros([11, 6984])
    i = 0

    for SOL_elements in SOL_str:
        SOLdata[:, i] = list(map(float, SOL_elements.split()))
        i = i + 1





    with open('DTCFILE.txt', 'r') as DTC:

        DTC_str = DTC.readlines()

    DTCdata = np.zeros([26, 6984])
    i = 0

    for DTC_elements in DTC_str:
        DTCdata[:, i] = list(map(float, DTC_elements.split()))
        i = i + 1







    with open('SOLRESAP.txt', 'r') as AP:

        AP_str = AP.readlines()

        APdata = np.zeros([12, 7011])
    i = 0

    for AP_elements in AP_str:

        APdata[:, i] = list(map(float, AP_elements.split()))
        i = i + 1









    return Cnm,Snm,eopdata,swdata,SOLdata,DTCdata,APdata


def test_Load_data():
    Load_data()


if __name__ == "__main__":
    test_Load_data()

