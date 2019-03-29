# #%--------------------------------------------------------------------------
# %
# %  finddays: finds the fractional days through a year given the year,month,
# %            day, hour, minute and second.
# %
# %  Inputs:
# %    year        - year                           1900 .. 2100
# %    mon         - month                          1 .. 12
# %    day         - day                            1 .. 28,29,30,31
# %    hr          - hour                           0 .. 23
# %    min         - minute                         0 .. 59
# %    sec         - second                         0.0 .. 59.999
# %
# %  Output:
# %    days        - day of year plus fraction of a
# %                  day                            days
# %
# %--------------------------------------------------------------------------
import numpy as np
def finddays(year, month, day, hr, min, sec):

    lmonth=np.zeros(12)
    for i in range(1,13):

        lmonth[i-1] = 31

        if i == 2:

            lmonth[i-1]= 28


        if i == 4 or i == 6 or i == 9 or i == 11:

            lmonth[i-1]= 30




    if (year-4*int(year/4) )== 0:

        lmonth[1]= 29

        if (year-100*int(year/100) == 0) and (year-400*int(year/400) != 0):

            lmonth[1]= 28




    i   = 1
    days = 0
    while (i < month) and ( i < 12 ):

        days= days + lmonth[i-1]
        i= i + 1


    days = days + day + hr/24 + min/1440 + sec/86400

    return days

def test():
    year=2016
    month=12
    day=23
    hr=2
    min=23
    sec=34

    days=finddays(year, month, day, hr, min, sec)

    print(days)



if __name__ == "__main__":

    test()