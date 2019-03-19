# #%--------------------------------------------------------------------------
# %
# % timediff: Time differences [s]
# %
def timediff(UT1_UTC,TAI_UTC):

    TT_TAI  = +32.184         # % TT-TAI time difference [s]

    GPS_TAI = -19.0          # % GPS-TAI time difference [s]

    TT_GPS  =  TT_TAI-GPS_TAI  #% TT-GPS time difference [s]

    TAI_GPS = -GPS_TAI         #% TAI-GPS time difference [s]

    UT1_TAI = UT1_UTC-TAI_UTC  #% UT1-TAI time difference [s]

    UTC_TAI = -TAI_UTC         #% UTC-TAI time difference [s]

    UTC_GPS = UTC_TAI-GPS_TAI  #% UTC_GPS time difference [s]

    UT1_GPS = UT1_TAI-GPS_TAI  #% UT1-GPS time difference [s]

    TT_UTC  = TT_TAI-UTC_TAI   #%  TT-UTC time difference [s]

    GPS_UTC = GPS_TAI-UTC_TAI  #% GPS-UTC time difference [s]

    return UT1_TAI,UTC_GPS,UT1_GPS,TT_UTC,GPS_UTC



def test_timediff():
    UT1_UTC=-0.6091681001888254
    TAI_UTC=35.0
    UT1_TAI, UTC_GPS, UT1_GPS, TT_UTC, GPS_UTC=timediff(UT1_UTC,TAI_UTC)

    print('UT1_TAI',UT1_TAI, 'UTC_GPS',UTC_GPS, 'UT1_GPS',UT1_GPS, 'TT_UTC',TT_UTC, 'GPS_UTC',GPS_UTC)


if __name__ == "__main__":

    test_timediff()