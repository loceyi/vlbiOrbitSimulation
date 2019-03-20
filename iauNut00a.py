
from scipy import io
from Const import Const
from numpy import  shape
from iauFal03 import iauFal03
from iauFaf03 import iauFaf03
def iauNut00a(date1, date2):

    const=Const()

    # % Units of 0.1 microarcsecond to radians
    U2R = const['DAS2R'] / 1e7

    # % -------------------------
    # % Luni-Solar nutation model
    # % -------------------------
    #
    # % The units for the sine and cosine coefficients are
    # % 0.1 microarcsecond and the same per Julian century
    #
    # % nl,nlp,nf,nd,nom:   coefficients of l,l',F,D,Om
    # % sp,spt,cp:          longitude sin, t*sin, cos coefficients
    # % ce,cet,se:          obliquity cos, t*cos, sin coefficients

    mat = io.loadmat('xls.mat')

    xls=mat['xls']


    # %  Number of terms in the luni-solar nutation model
    temporary_parameter = shape(xls)
    NLS=temporary_parameter[0]

    # %  ------------------------
    # %  Planetary nutation model
    # %  ------------------------
    #
    # %  The units for the sine and cosine coefficients are
    # %  0.1 microarcsecond
    #
    # % nl, nf, nd, nom     coefficients of l, F, D and Omega
    # % nme, nve, nea, nma, nju, nsa, nur, nne  coefficients of planetary longitudes
    # % npa                 coefficient of general precession
    # % sp,cp               longitude sin, cos coefficients
    # % se,ce               obliquity sin, cos coefficients
    mat = io.loadmat('xpl.mat')

    xpl = mat['xpl']

    # % Number of terms in the planetary nutation model
    temporary_parameter = shape(xpl)
    NPL = temporary_parameter[0]

    # % --------------------------------------------------------------------

    # % Interval between fundamental date J2000.0 and given date (JC).
    t = ((date1 - const['DJ00']) + date2) / const['DJC']

    # % -------------------
    # % LUNI-SOLAR NUTATION
    # % -------------------
    #
    # % Fundamental (Delaunay) arguments
    #
    # % Mean anomaly of the Moon (IERS 2003).
    el = iauFal03(t)

    # % Mean anomaly of the Sun (MHB2000)
    elp = ((1287104.79305  +
              t * (129596581.0481  +
              t * (-0.5532   +
              t * (0.000136  +
              t * (-0.00001149)))))% const.TURNAS) * const['DAS2R']

    # % Mean longitude of the Moon minus that of the ascending node (IERS 2003).

    f = iauFaf03(t)

    # % Mean elongation of the Moon from the Sun (MHB2000).
    d = ((1072260.70369  +
            t * (1602961601.2090  +
            t * (-6.3706  +
            t * (0.006593  +
            t * (-0.00003169)))))% const['TURNAS'])*const['DAS2R']

    # % Mean longitude of the ascending node of the Moon (IERS 2003).
    om = iauFaom03(t);

    % Initialize the nutation values.
    dp = 0.0;
    de = 0.0;

    % Summation of luni-solar nutation series (in reverse order).
    for i = NLS:-1:1
        % Argument and functions.
        arg = mod(xls(i,1) * el + xls(i,2) * elp + xls(i,3) * f + xls(i,4) * d +...
                  xls(i,5) * om, const.D2PI);
        sarg = sin(arg);
        carg = cos(arg);

        % Term
        dp = dp + (xls(i,6) + xls(i,7) * t) * sarg + xls(i,8) * carg;
        de = de + (xls(i,9) + xls(i,10) * t) * carg + xls(i,11) * sarg;
    end

    % Convert from 0.1 microarcsec units to radians.
    dpsils = dp * U2R;
    depsls = de * U2R;

    % ------------------
    % PLANETARY NUTATION
    % ------------------

    %  n.b.  The MHB2000 code computes the luni-solar and planetary nutation
    %  in different functions, using slightly different Delaunay
    %  arguments in the two cases.  This behaviour is faithfully
    %  reproduced here.  Use of the IERS 2003 expressions for both
    %  cases leads to negligible changes, well below
    %  0.1 microarcsecond.

    % Mean anomaly of the Moon (MHB2000).
    al = mod(2.35555598 + 8328.6914269554 * t, const.D2PI);

    % Mean longitude of the Moon minus that of the ascending node (MHB2000).
    af = mod(1.627905234 + 8433.466158131 * t, const.D2PI);

    % Mean elongation of the Moon from the Sun (MHB2000)
    ad = mod(5.198466741 + 7771.3771468121 * t, const.D2PI);

    % Mean longitude of the ascending node of the Moon (MHB2000)
    aom = mod(2.18243920 - 33.757045 * t, const.D2PI);

    % General accumulated precession in longitude (IERS 2003)
    apa = (0.024381750 + 0.00000538691 * t) * t;

    % Mean longitude of Mercury (IERS Conventions 2003)
    alme = mod(4.402608842 + 2608.7903141574 * t, const.D2PI);

    % Mean longitude of Venus (IERS Conventions 2003)
    alve = mod(3.176146697 + 1021.3285546211 * t, const.D2PI);

    % Mean longitude of Earth (IERS Conventions 2003)
    alea = mod(1.753470314 + 628.3075849991 * t, const.D2PI);

    % Mean longitude of Mars (IERS Conventions 2003)
    alma = mod(6.203480913 + 334.0612426700 * t, const.D2PI);

    % Mean longitude of Jupiter (IERS Conventions 2003)
    alju = mod(0.599546497 + 52.9690962641 * t, const.D2PI);

    % Mean longitude of Saturn (IERS Conventions 2003)
    alsa = mod(0.874016757 + 21.3299104960 * t, const.D2PI);

    % Mean longitude of Uranus (IERS Conventions 2003)
    alur = mod(5.481293872 + 7.4781598567 * t, const.D2PI);

    % Neptune longitude (MHB2000).
    alne = mod(5.321159000 + 3.8127774000 * t, const.D2PI);

    % Initialize the nutation values.
    dp = 0.0;
    de = 0.0;

    % Summation of planetary nutation series (in reverse order).
    for i = NPL:-1:1
        % Argument and functions.
        arg = mod(xpl(i,1) * al   + xpl(i,2) * af   + xpl(i,3) * ad   +...
                  xpl(i,4) * aom  + xpl(i,5) * alme + xpl(i,6) * alve +...
                  xpl(i,7) * alea + xpl(i,8) * alma + xpl(i,9) * alju +...
                  xpl(i,10)* alsa + xpl(i,11)* alur + xpl(i,12)* alne +...
                  xpl(i,13)* apa, const.D2PI);
        sarg = sin(arg);
        carg = cos(arg);

        % Term.
        dp = dp + xpl(i,14) * sarg + xpl(i,15) * carg;
        de = de + xpl(i,16) * sarg + xpl(i,17) * carg;
    end

    % Convert from 0.1 microarcsec units to radians.
    dpsipl = dp * U2R;
    depspl = de * U2R;

    % -------
    % RESULTS
    % -------

    % Add luni-solar and planetary components.
    dpsi = dpsils + dpsipl;
    deps = depsls + depspl;

    return dpsi deps