"""Concrete date/time and related types.
See http://www.iana.org/time-zones/repository/tz-link.html for
time zone and DST data sources.
"""

__all__ = ("date", "MINYEAR", "MAXYEAR")

import time as _time
from operator import index as _index


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


MINYEAR = 1
MAXYEAR = 9999
# _MAXORDINAL = 3652059  # date.max.toordinal()
_MAXORDINAL = 3651695

# Utility functions, adapted from Python's Demo/classes/Dates.py, which
# also assumes the current Gregorian calendar indefinitely extended in
# both directions.  Difference:  Dates.py calls January 1 of year 0 day
# number 1.  The code here calls January 1 of year 1 day number 1.  This is
# to match the definition of the "proleptic Gregorian" calendar in Dershowitz
# and Reingold's "Calendrical Calculations", where it's the base calendar
# for all computations.  See the book for algorithms for converting between
# proleptic Gregorian ordinals and many other calendar systems.

# -1 is a placeholder for indexing purposes.

_GREGORIAN_DAY_AT_END_OF_BANGLA_MONTH = [
    -1, 14, 13, 14, 13, 14, 14, 15, 15, 15, 16, 15, 15
]

_BANGLA_DAY_AT_GREGORIAN_MONTH_START = [
    -1, 17, 18, 16, 18, 18, 18, 17, 17, 17, 16, 16, 16
]

_BANGLA_DAY_AT_GREGORIAN_MONTH_END = [
    -1, 17, 15, 17, 17, 17, 16, 16, 16, 15, 15, 15, 16
]

_DAYS_IN_GREGORIAN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_IN_BANGLA_MONTH = [-1, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 29, 30]

_MONTHNAMES = [
    None, "Bois", "Jyoi", "Asha", "Shra", "Bhad", "Ashs", "Kart", "Ogro",
    "Pous", "Magh", "Falg", "Choi"
]
_DAYNAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_BANGLA_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim


def _is_leap(year):
    year = year + 594
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# def _days_before_year(year):  # this funtion needs further checking
#     "year -> number of days before January 1st of year."
#     y = year - 1
#     return y * 365 + y // 4 - y // 100 + y // 400


def _days_before_year(year):  # this funtion needs further checking
    "year -> number of days before January 1st of year."
    y = year - 1
    yy = y + 594
    # yy is gregorian year respective to bangla year
    # and 144 is number of gregorian leap years till 594
    return y * 365 + yy // 4 - yy // 100 + yy // 400 - 144


def _gregorian_day_at_bangla_month_end(gregorian_year, gregorian_month):
    """
    gregorian_year, gregorian_month -> number of days in that month in that
    year.
    """
    assert 1 <= gregorian_month <= 12, gregorian_month
    return _GREGORIAN_DAY_AT_END_OF_BANGLA_MONTH[gregorian_month]


def _bangla_day_at_gregorian_month_end(gregorian_year, gregorian_month):
    """
    gregorian_year, gregorian_month -> number of days in that month in that
    year.
    """
    assert 1 <= gregorian_month <= 12, gregorian_month
    if gregorian_month == 2 and _is_leap(gregorian_year - 594):
        return 16
    return _BANGLA_DAY_AT_GREGORIAN_MONTH_END[gregorian_month]


def _bangla_day_at_gregorian_month_start(gregorian_year, gregorian_month):
    """
    gregorian_year, gregorian_month -> number of days in that month in that
    year.
    """
    assert 1 <= gregorian_month <= 12, gregorian_month
    if gregorian_month == 3 and _is_leap(gregorian_year - 594):
        return 17
    return _BANGLA_DAY_AT_GREGORIAN_MONTH_START[gregorian_month]


def _days_in_gregorian_month(gregorian_year, gregorian_month):
    """
    gregorian_year, gregorian_month -> number of days in that gregorian month
    in that gregorian year.
    """
    assert 1 <= gregorian_month <= 12, gregorian_month
    if gregorian_month == 2 and _is_leap(gregorian_year - 594):
        return 29
    return _DAYS_IN_GREGORIAN_MONTH[gregorian_month]


def _days_in_month(year, month):
    "year, month -> number of days in that bangla month in that bangla year."
    assert 1 <= month <= 12, month
    if month == 11 and _is_leap(year):
        return 30
    return _DAYS_IN_BANGLA_MONTH[month]


def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, 'month must be in 1..12'
    return _DAYS_BEFORE_MONTH[month] + (month > 11 and _is_leap(year))


def _ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, 'month must be in 1..12'
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
    return (_days_before_year(year) + _days_before_month(year, month) + day)


_DI400Y = _days_before_year(401)  # number of days in 400 years
_DI100Y = _days_before_year(101)  # number of days in 100 years
_DI4Y = _days_before_year(5)  # number of days in 4 years

# A 4-year cycle has an extra leap day over what we'd get from pasting
# together 4 single years.
assert _DI4Y == 4 * 365 + 1

# Similarly, a 400-year cycle has an extra leap day over what we'd get from
# pasting together 4 100-year cycles.
assert _DI400Y == 4 * _DI100Y + 1

# OTOH, a 100-year cycle has one fewer leap day than we'd get from
# pasting together 25 4-year cycles.
assert _DI100Y == 25 * _DI4Y - 1


def _ord2md(year, od):

    bar = 365 + _is_leap(year)
    if not 1 <= od <= bar:
        raise ValueError('Ordinal date must be in 1..%d' % bar, od)
    for month in range(12, 0, -1):
        before = _days_before_month(year, month)
        if od > before:
            day = od - before
            year, month, day = _check_date_fields(year, month, day)
            return (month, day)


def _ord2ymd(n):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."
    if not 1 <= n <= _MAXORDINAL:
        raise ValueError('Ordinal date must be in 1..3651695', n)
    """
        Boishakh 1, 0001 is ordinal date 1
    """
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400  # ..., -399, 1, 401, ...
    n100, n = divmod(n, _DI100Y)
    year += n100 * 100
    n4, n = divmod(n, _DI4Y)
    year += n4 * 4

    isleappossible = True
    if n4 == 1:
        isleappossible = False
    if n100 == 2:
        isleappossible = True
    if n4 >= 2:
        n += 1
    if (n100 == 2 and n4 >= 2) or (n100 > 2):
        n -= 1

    if n == 730 and isleappossible:
        return year + 2, 12, 30
    if n >= 731 and isleappossible:
        n -= isleappossible

    n1, n = divmod(n, 365)

    year += n1 + 1

    if isleappossible and n1 == 1:
        dumpyear = 2
    else:
        dumpyear = 1
    month, day = _ord2md(dumpyear, n + 1)
    return year, month, day


def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 6) % 7
    dnum = _days_before_month(y, m) + d
    return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _format_time(hh, mm, ss, us, timespec='auto'):
    specs = {
        'hours': '{:02d}',
        'minutes': '{:02d}:{:02d}',
        'seconds': '{:02d}:{:02d}:{:02d}',
        'milliseconds': '{:02d}:{:02d}:{:02d}.{:03d}',
        'microseconds': '{:02d}:{:02d}:{:02d}.{:06d}'
    }

    if timespec == 'auto':
        # Skip trailing microseconds when us==0.
        timespec = 'microseconds' if us else 'seconds'
    elif timespec == 'milliseconds':
        us //= 1000
    try:
        fmt = specs[timespec]
    except KeyError:
        raise ValueError('Unknown timespec value')
    else:
        return fmt.format(hh, mm, ss, us)


# Helpers for parsing the result of isoformat()
def _parse_isoformat_date(dtstr):
    # It is assumed that this function will only be called with a
    # string of length exactly 10, and (though this is not used) ASCII-only
    year = int(dtstr[0:4])
    if dtstr[4] != '-':
        raise ValueError('Invalid date separator: %s' % dtstr[4])

    month = int(dtstr[5:7])

    if dtstr[7] != '-':
        raise ValueError('Invalid date separator')

    day = int(dtstr[8:10])

    return [year, month, day]


def _parse_hh_mm_ss_ff(tstr):
    # Parses things of the form HH[:MM[:SS[.fff[fff]]]]
    len_str = len(tstr)

    time_comps = [0, 0, 0, 0]
    pos = 0
    for comp in range(0, 3):
        if (len_str - pos) < 2:
            raise ValueError('Incomplete time component')

        time_comps[comp] = int(tstr[pos:pos + 2])

        pos += 2
        next_char = tstr[pos:pos + 1]

        if not next_char or comp >= 2:
            break

        if next_char != ':':
            raise ValueError('Invalid time separator: %c' % next_char)

        pos += 1

    if pos < len_str:
        if tstr[pos] != '.':
            raise ValueError('Invalid microsecond component')
        else:
            pos += 1

            len_remainder = len_str - pos
            if len_remainder not in (3, 6):
                raise ValueError('Invalid microsecond component')

            time_comps[3] = int(tstr[pos:])
            if len_remainder == 3:
                time_comps[3] *= 1000

    return time_comps


# Just raise TypeError if the arg isn't None or a string.
def _check_tzname(name):
    if name is not None and not isinstance(name, str):
        raise TypeError("tzinfo.tzname() must return None or string, "
                        "not '%s'" % type(name))


def _check_gregorian_date_fields(year, month, day):
    year = _index(year)
    month = _index(month)
    day = _index(day)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12', month)
    dim = _days_in_gregorian_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError('day must be in 1..%d' % dim, day)
    return year, month, day


def _check_date_fields(year, month, day):
    year = _index(year)
    month = _index(month)
    day = _index(day)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12', month)
    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError('day must be in 1..%d' % dim, day)
    return year, month, day


def _check_time_fields(hour, minute, second, microsecond, fold):
    hour = _index(hour)
    minute = _index(minute)
    second = _index(second)
    microsecond = _index(microsecond)
    if not 0 <= hour <= 23:
        raise ValueError('hour must be in 0..23', hour)
    if not 0 <= minute <= 59:
        raise ValueError('minute must be in 0..59', minute)
    if not 0 <= second <= 59:
        raise ValueError('second must be in 0..59', second)
    if not 0 <= microsecond <= 999999:
        raise ValueError('microsecond must be in 0..999999', microsecond)
    if fold not in (0, 1):
        raise ValueError('fold must be either 0 or 1', fold)
    return hour, minute, second, microsecond, fold


def _cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" %
                    (type(x).__name__, type(y).__name__))


def _divide_and_round(a, b):
    """divide a by b and round result to the nearest integer
    When the ratio is exactly half-way between two integers,
    the even integer is returned.
    """
    # Based on the reference implementation for divmod_near
    # in Objects/longobject.c.
    q, r = divmod(a, b)
    # round up if either r / b > 0.5, or r / b == 0.5 and q is odd.
    # The expression r / b > 0.5 is equivalent to 2 * r > b if b is
    # positive, 2 * r < b if b negative.
    r *= 2
    greater_than_half = r > b if b > 0 else r < b
    if greater_than_half or r == b and q % 2 == 1:
        q += 1

    return q


def _isoweek1monday(year):
    # Helper to calculate the day number of the Monday starting week 1
    # XXX This could be done more efficiently
    THURSDAY = 3
    firstday = _ymd2ord(year, 1, 1)
    firstweekday = (firstday + 6) % 7  # See weekday() above
    week1monday = firstday - firstweekday
    if firstweekday > THURSDAY:
        week1monday += 7
    return week1monday


class date:
    """Concrete date type.
    Constructors:
    __new__()
    fromtimestamp()
    today()
    fromordinal()
    Operators:
    __repr__, __str__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__ (add/radd only with timedelta arg)
    Methods:
    timetuple()
    toordinal()
    weekday()
    isoweekday(), isocalendar(), isoformat()
    ctime()
    strftime()
    Properties (readonly):
    year, month, day
    """
    __slots__ = '_year', '_month', '_day', '_hashcode'

    def __new__(cls, year, month=None, day=None):
        """Constructor.
        Arguments:
        year, month, day (required, base 1)
        """
        if (month is None and isinstance(year, (bytes, str)) and len(year) == 4
                and 1 <= ord(year[2:3]) <= 12):
            # Pickle support
            if isinstance(year, str):
                try:
                    year = year.encode('latin1')
                except UnicodeEncodeError:
                    # More informative error message.
                    raise ValueError(
                        "Failed to encode latin1 string when unpickling "
                        "a date object. "
                        "pickle.load(data, encoding='latin1') is assumed.")
            self = object.__new__(cls)
            self.__setstate(year)
            self._hashcode = -1
            return self
        year, month, day = _check_date_fields(year, month, day)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    # Additional constructors

    @classmethod
    def fromgregorian(cls,
                      gregorian_year=None,
                      gregorian_month=None,
                      gregorian_day=None):

        gregorian_year, gregorian_month, gregorian_day = \
            _check_gregorian_date_fields(gregorian_year,
                                         gregorian_month,
                                         gregorian_day)

        bar = gregorian_month < 4 or \
            (gregorian_month == 4 and gregorian_day < 14)
        bangla_year = gregorian_year - 593 - bar

        foo = _gregorian_day_at_bangla_month_end(gregorian_year,
                                                 gregorian_month)
        if gregorian_day <= foo:
            bangla_month = (gregorian_month + 8) % 12 or 12
            bangla_day = gregorian_day + (_bangla_day_at_gregorian_month_start(
                gregorian_year, gregorian_month) - 1)
        else:
            bangla_month = (gregorian_month + 9) % 12 or 12
            bangla_day = gregorian_day - (
                _days_in_gregorian_month(gregorian_year, gregorian_month) -
                _bangla_day_at_gregorian_month_end(gregorian_year,
                                                   gregorian_month))
        return cls(bangla_year, bangla_month, bangla_day)

    @classmethod
    def fromtimestamp(cls, t):
        "Construct a date from a POSIX timestamp (like time.time())."
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.localtime(t)
        print("called from date class fromtimestamp method")
        return cls.fromgregorian(y, m, d)

    @classmethod
    def today(cls):
        "Construct a date from time.time()."
        t = _time.time()
        return cls.fromtimestamp(t)

    @classmethod
    def fromordinal(cls, n):
        """Construct a date from a proleptic Gregorian ordinal.
        January 1 of year 1 is day 1.  Only the year, month and day are
        non-zero in the result.
        """
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a date from the output of date.isoformat()."""
        if not isinstance(date_string, str):
            raise TypeError('fromisoformat: argument must be str')

        try:
            assert len(date_string) == 10
            return cls(*_parse_isoformat_date(date_string))
        except Exception:
            raise ValueError(f'Invalid isoformat string: {date_string!r}')

    # Conversions to string

    def __repr__(self):
        """Convert to formal string, for repr().
        >>> dt = datetime(2010, 1, 1)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0)'
        >>> dt = datetime(2010, 1, 1, tzinfo=timezone.utc)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)'
        """
        return "%s.%s(%d, %d, %d)" % (self.__class__.__module__,
                                      self.__class__.__qualname__, self._year,
                                      self._month, self._day)

    # XXX These shouldn't depend on time.localtime(), because that
    # clips the usable dates to [1970 .. 2038).  At least ctime() is
    # easily done without using strftime() -- that's better too because
    # strftime("%c", ...) is locale specific.

    def ctime(self):
        "Return ctime() style string."
        weekday = self.toordinal() % 7 or 7
        return "%s %s %2d 00:00:00 %04d" % (_DAYNAMES[weekday],
                                            _MONTHNAMES[self._month],
                                            self._day, self._year)

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError("must be str, not %s" % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def isoformat(self):
        """Return the date formatted according to ISO.
        This is 'YYYY-MM-DD'.
        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        return "%04d-%02d-%02d" % (self._year, self._month, self._day)

    __str__ = isoformat

    # Read-only field accessors
    @property
    def year(self):
        """year (1-9999)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month

    @property
    def day(self):
        """day (1-31)"""
        return self._day

    # Standard conversions, __eq__, __le__, __lt__, __ge__, __gt__,
    # __hash__ (and helpers)

    def timetuple(self):
        "Return local time tuple compatible with time.localtime()."
        return _build_struct_time(self._year, self._month, self._day, 0, 0, 0,
                                  -1)

    def toordinal(self):
        """Return proleptic Gregorian ordinal for the year, month and day.
        January 1 of year 1 is day 1.  Only the year, month and day values
        contribute to the result.
        """
        return _ymd2ord(self._year, self._month, self._day)

    def replace(self, year=None, month=None, day=None):
        """Return a new date with new values for the specified fields."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        return type(self)(year, month, day)

    # Comparisons of date objects with other.

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, date)
        y, m, d = self._year, self._month, self._day
        y2, m2, d2 = other._year, other._month, other._day
        return _cmp((y, m, d), (y2, m2, d2))

    def __hash__(self):
        "Hash."
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode

    # Computations

    def weekday(self):
        "Return day of the week, where Monday == 0 ... Sunday == 6."
        return (self.toordinal() + 6) % 7

    # Day-of-the-week and week-of-the-year, according to ISO

    def isoweekday(self):
        "Return day of the week, where Monday == 1 ... Sunday == 7."
        # 1-Jan-0001 is a Monday
        return self.toordinal() % 7 or 7

    def isocalendar(self):
        """Return a named tuple containing ISO year, week number, and weekday.
        The first ISO week of the year is the (Mon-Sun) week
        containing the year's first Thursday; everything else derives
        from that.
        The first week is 1; Monday is 1 ... Sunday is 7.
        ISO calendar algorithm taken from
        http://www.phys.uu.nl/~vgent/calendar/isocalendar.htm
        (used with permission)
        """
        year = self._year
        week1monday = _isoweek1monday(year)
        today = _ymd2ord(self._year, self._month, self._day)
        # Internally, week and day have origin 0
        week, day = divmod(today - week1monday, 7)
        if week < 0:
            year -= 1
            week1monday = _isoweek1monday(year)
            week, day = divmod(today - week1monday, 7)
        elif week >= 52:
            if today >= _isoweek1monday(year + 1):
                year += 1
                week = 0
        return year, week + 1, day + 1

    # Pickle support.

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        return bytes([yhi, ylo, self._month, self._day]),

    def __setstate(self, string):
        yhi, ylo, self._month, self._day = string
        self._year = yhi * 256 + ylo

    def __reduce__(self):
        return (self.__class__, self._getstate())


# _date_class = date  # so functions w/ args named "date" can get at the class

# date.min = date(1, 1, 1)
# date.max = date(9999, 12, 30)

# try:
#     from _bangladatetime import *
# except ImportError:
#     pass
# else:
#     # Clean up unused names
#     del (_GREGORIAN_DAY_AT_END_OF_BANGLA_MONTH,
#          _BANGLA_DAY_AT_GREGORIAN_MONTH_START,
#          _BANGLA_DAY_AT_GREGORIAN_MONTH_END, _DAYS_IN_GREGORIAN_MONTH,
#          _DAYS_IN_BANGLA_MONTH, _DAYNAMES, _DAYS_BEFORE_MONTH, _DI100Y,
#          _DI400Y, _DI4Y, _MAXORDINAL, _MONTHNAMES, _build_struct_time,
#          _check_date_fields, _check_time_fields, _check_tzname, _cmp,
#          _cmperror, _date_class, _days_before_month, _days_before_year,
#          _days_in_month, _format_time, _is_leap, _isoweek1monday, _ord2ymd,
#          _time, _ymd2ord, _divide_and_round)
#     # XXX Since import * above excludes names that start with _,
#     # docstring does not get overwritten. In the future, it may be
#     # appropriate to maintain a single module level docstring and
#     # remove the following line.
#     from _datetime import __doc__
