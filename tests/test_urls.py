# -*- coding: utf-8 -*-
from trackmaven_common.urls import (
    httpsify, parse_domain, clean_url, validate_url)
import pytest


def test_httpsify_http():
    """
    Test should return `https://test.local`
    """
    url = 'http://test.local'
    assert httpsify(url) == 'https://test.local'


def test_httpsify_https():
    """
    Test should return `https://test.local`
    """
    url = 'https://test.local'
    assert httpsify(url) == 'https://test.local'


def test_parse_domain():
    """
    Test should return google.com
    """
    url = 'http://www.google.com'
    assert parse_domain(url) == 'google.com'


def test_clean_url_no_http():
    assert 'http://www.trackmaven.com/' == clean_url('www.trackmaven.com')


def test_clean_url_no_slash():
    assert 'http://www.trackmaven.com/' == clean_url('http://www.trackmaven.com')


def test_clean_url_white_space():
    assert 'http://www.trackmaven.com/' == clean_url('http://www.trackmaven.com  ')


def test_clean_url_unicode():
    assert u'http://trackmaven.com/' == clean_url(u'http://trackmaven.com/∞')


def test_validate_url_valid():
    assert validate_url('http://trackmaven.com/') == 'http://trackmaven.com/'


def test_validate_url_invalid():
    with pytest.raises(ValueError) as exc:
        validate_url('_rackmaven.c1m/')
    assert str(exc.value) == "Enter a valid URL."
