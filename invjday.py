#%  hr		hour
# %  min		minute
# %  sec		second
# %
# %  note: day may include fractional part
from math import floor

def invjday(jd):

    z = int(jd + .5)
    fday = jd + .5 - z

    if (fday < 0):

       fday = fday + 1
       z = z - 1


    if (z < 2299161):

       a = z
    else:

       alpha = floor((z - 1867216.25) / 36524.25)
       a = z + 1 + alpha - floor(alpha / 4)


    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + fday

    if (e < 14):

       month = e - 1

    else:

       month = e - 13



    if (month > 2):

       year = c - 4716

    else:

       year = c - 4715



    hr = abs(day-floor(day))*24
    min = abs(hr-floor(hr))*60
    sec = abs(min-floor(min))*60

    day = floor(day)
    hr = floor(hr)
    min = floor(min)

    return year, month, day, hr, min, sec


def test_invjday():
    jd=2457137.4135185187
    year, month, day, hr, min, sec=invjday(jd)

    print('year',year, 'month',month, 'day',day, 'hr',hr, 'min',min,'sec',sec)


if __name__ == "__main__":

    test_invjday()