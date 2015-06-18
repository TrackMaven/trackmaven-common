import re
try:
    from urllib.parse import urlsplit, urlunsplit, urlparse
except ImportError:
    from urlparse import urlsplit, urlunsplit, urlparse


def httpsify(url):
    """
    Takes a URL and returns the URL with the HTTPS protocol.

    Example:

    >>> httpsify("http://test.com")
    "https://test.com"
    """
    if url.lower().find('http:') == 0:
        url = url.replace('http', 'https', 1)

    return url


def parse_domain(url):
    """
    Returns just the domain part of a URL.

    Example:

    >>> parse_domain("http://trackmaven.com/blog/")
    "trackmaven.com"
    >>>
    """
    if not url:
        return None
    parsed_url = urlparse(url)
    if url.startswith('http'):
        domain = parsed_url.netloc
    else:
        domain = parsed_url.path
    return domain.replace('www.', '')


def clean_url(value):
    """
    Taken from Django' URLField, this helps to normalize URLs. Raises a
    ValueError if an invalid url is passed.

    Example:

    >>> clean_url("www.google.com")
    "http://www.google.com"

    >>> clean_url("_.com")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Enter a valid URL.
    """
    if value:
        value = value.strip()
        value = value.encode('ascii', 'ignore').decode("utf-8")
        url_fields = list(urlsplit((value)))
        if not url_fields[0]:
            # If no URL scheme given, assume http://
            url_fields[0] = 'http'
        if not url_fields[1]:
            # Assume that if no domain is provided, that the path segment
            # contains the domain.
            url_fields[1] = url_fields[2]
            url_fields[2] = ''
            # Rebuild the url_fields list, since the domain segment may now
            # contain the path too.
            url_fields = list(urlsplit((urlunsplit(url_fields))))
        if not url_fields[2]:
            # the path portion may need to be added before query params
            url_fields[2] = '/'
        value = urlunsplit(url_fields)
    return value


def validate_url(value):
    """
    Taken from Django' URLField. Attempts to check if a url is valid, if not
    raises a ValueError()

    Example:

    >>> validate_url("http://www.valid.com")
    "http://www.valid.com"

    >>> validate_url("_.com")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Enter a valid URL.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not regex.search(value):
        raise ValueError("Enter a valid URL.")
    return value
