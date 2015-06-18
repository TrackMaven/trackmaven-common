from trackmaven_common.lists import split_every, uniquify
from datetime import date


def test_split_every_even():
    split = split_every([1, 2, 3, 4], 2)
    assert split == [[1, 2], [3, 4]]


def test_split_every_odd():
    split = split_every([1, 2, 3, 4, 5], 2)
    assert split == [[1, 2], [3, 4], [5]]


def test_uniquify():
    l = [
        {"a": 1, "b": 2},
        {"b": 2, "a": 1},
        {"foo": "bar"},
        {"foo": "boo"},
        {"foo": "bar"},
        {"bar": "foo"},
        {"date": date(2014, 1, 1)},
        {"date": date(2014, 1, 1)}
    ]

    expected = [
        {"a": 1, "b": 2},
        {"foo": "bar"},
        {"foo": "boo"},
        {"bar": "foo"},
        {"date": date(2014, 1, 1)}
    ]
    assert uniquify(l) == expected
