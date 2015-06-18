from trackmaven_common.dates import iso_to_utc, daily_date_range, force_to_date

from pytz import UTC
from datetime import datetime, date
import pytest


def test_iso_to_utc_case_1():
    expected = datetime(2014, 7, 3, tzinfo=UTC)
    timestamp = iso_to_utc("2014-07-03 00:00:00")
    # Check the timestamp is datetime aware.
    assert timestamp.tzinfo is not None
    assert timestamp == expected


def test_iso_to_utc_case_2():
    timestamp = iso_to_utc("2014-01-01 00:00:00")
    expected = datetime(2014, 1, 1, tzinfo=UTC)
    # Check the timestamp is datetime aware.
    assert timestamp.tzinfo is not None
    assert timestamp == expected


def test_daily_date_range():
    timestamp = date(2014, 1, 1)
    expected = [
        date(2014, 1, 1),
        date(2014, 1, 2),
        date(2014, 1, 3),
        date(2014, 1, 4)]

    actual = daily_date_range(timestamp, 3)
    assert expected == actual


def test_force_to_date_date():
    d1 = date(2014, 1, 1)
    d2 = force_to_date(d1)
    assert d2 == d1


def test_force_to_date_datetime():
    d1 = datetime(2014, 1, 1)
    d2 = force_to_date(d1)
    assert d2, date(2014, 1 == 1)


def test_force_to_date_invalid():
    with pytest.raises(TypeError):
        force_to_date("test")
