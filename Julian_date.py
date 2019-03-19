from math import floor

def Julian_date(month,day,year,hour,minute,second):
    '''

    :param month: calendar month[1~12]
    :param day: [1~31]
    :param year: [yyyy]
    :return: Julian date

    '''
    y = year
    m = month
    b = 0
    c = 0

    if m<=2 :

        y = y-1
        m = m + 12

    if y<0 :

        c=-0.75

    if year < 1582:

        pass

    elif year > 1582:

        a =  int(y/100)
        b = 2 - a + floor(a/4)

    elif month < 10 :

        pass

    elif month > 10 :

        a= int(y/100)
        b=2 -a+floor(a/4)


    elif day <=4:

        pass

    elif day >14:

        a=int(y/100)
        b=2-a+floor(a/4)


    else:

        print('this is an invalid calendar date!')


    jd=int(365.25*y+c)+int(30.6001*(m+1))
    Julian_date=jd+day+b+1720994.5
    hour=hour/24
    minute=(minute/60)/24
    second=(second/3600)/24
    Julian_date=Julian_date+hour+minute+second




    return Julian_date


def Mjd(month, day, year, hour, minute, second):
    '''

    :param month: calendar month[1~12]
    :param day: [1~31]
    :param year: [yyyy]
    :return: Julian date

    '''
    y = year
    m = month
    b = 0
    c = 0

    if m <= 2:
        y = y - 1
        m = m + 12

    if y < 0:
        c = -0.75

    if year < 1582:

        pass

    elif year > 1582:

        a = int(y / 100)
        b = 2 - a + floor(a / 4)

    elif month < 10:

        pass

    elif month > 10:

        a = int(y / 100)
        b = 2 - a + floor(a / 4)


    elif day <= 4:

        pass

    elif day > 14:

        a = int(y / 100)
        b = 2 - a + floor(a / 4)


    else:

        print('this is an invalid calendar date!')

    jd = int(365.25 * y + c) + int(30.6001 * (m + 1))
    Julian_date = jd + day + b + 1720994.5
    hour = hour / 24
    minute = (minute / 60) / 24
    second = (second / 3600) / 24
    Julian_date = Julian_date + hour + minute + second

    Mjd=Julian_date-2400000.5

    return Mjd

def test():
    month=12
    day=1
    year=2018
    hour=12
    minute=0
    second=0
    jd=Julian_date(month,day,year,hour,minute,second)
    print(jd)



if __name__ == "__main__":

    test()








