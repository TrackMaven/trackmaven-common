import arrow
from datetime import timedelta, datetime, date
from dateutil import parser
import pytz


def today():
    """
    Return today's datetime.

    Example:

    >>> today()
    datetime.datetime(2015, 6, 18, 15, 6, 59, 787694, tzinfo=tzutc())

    """
    return arrow.utcnow().datetime

now = today


def last_week():
    """
    Returns last week's datetime.

    Example:

    >>> last_week()
    datetime.datetime(2015, 6, 11, 15, 7, 12, 840317, tzinfo=tzutc())
    """
    return arrow.utcnow().replace(days=-7).datetime


def last_month():
    """
    Returns last month's datetime.

    Example:

    >>> last_month()
    datetime.datetime(2015, 5, 19, 15, 7, 30, 693635, tzinfo=tzutc())
    """
    return arrow.utcnow().replace(days=-30).datetime


def seconds_since_epoch(date):
    """
    Returns total seconds since 1/1/1970 (UTC timezone)

    Example:

    >>> d = datetime.datetime(2015, 6, 11, 15, 7, 12, 840317, tzinfo=tzutc())
    >>> seconds_since_epoch(d)
    1434640140
    """
    epoch = arrow.get(0).datetime.replace(tzinfo=pytz.utc)
    return int((date - epoch).total_seconds())


def days_since_epoch(date):
    """
    Returns the total days since 1/1/1970 (UTC timezone)

    Example:

    >>> d = datetime.date(2014, 6, 11)
    >>> days_since_epoch(d)
    16604
    """
    epoch = arrow.get(0).datetime.replace(tzinfo=pytz.utc).date()
    return int((date - epoch).days)


def iso_to_utc(iso):
    """
    Returns an ISO 8601 timestamp into a python datetime object with a utc tz.

    Example:

    >>> iso_to_utc("2014-07-03 00:00:00")
    datetime(2014, 07, 03, 0, 0, 0, tz="utc")
    """
    timestamp = parser.parse(iso)
    timestamp = timestamp.replace(tzinfo=pytz.utc)
    return timestamp


def daily_date_range(date, days_ahead):
    """
    Returns a list of future dates for a number of days ahead from
    a start date. Start date is included.

    Example:

    >>> d = datetime.date(2014, 6, 11)
    >>> daily_date_range(d, 3)
    [datetime.datetime(2015, 6, 18, 15, 9, 0, 490145, tzinfo=tzutc()), datetime.datetime(2015, 6, 19, 15, 9, 0, 490145, tzinfo=tzutc()), datetime.datetime(2015, 6, 20, 15, 9, 0, 490145, tzinfo=tzutc()), datetime.datetime(2015, 6, 21, 15, 9, 0, 490145, tzinfo=tzutc())]

    """
    date_range = []
    for day in range(days_ahead + 1):
        date_range.append(date + timedelta(days=day))
    return date_range


def date_key_to_iso(short_date):
    """
    Convert a 6-digit date string from java formatted date to ISO.

    Example:

    >>> java_date = '140101'
    >>> date_key_to_iso(java_date)
    '2014-01-01'

    """
    return '-'.join(['20' + short_date[0:2],
                    short_date[2:4], short_date[4:6]])


def force_to_date(obj):
    """
    Converts a datetime object into a date.

    Example:

    >>> d = datetime.datetime(2015, 6, 18, 15, 9, 0, 490145, tzinfo=tzutc())
    >>> force_to_date(d)
    datetime.date(2015, 6, 18)
    """
    if type(obj) is date:
        return obj
    elif type(obj) is datetime:
        return obj.date()
    raise TypeError('Must be a datetime.date or datetime.datetime, not %s' % type(obj))
