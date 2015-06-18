from bs4 import BeautifulSoup
import re


def clean_string(string):
    """
    Cleans up a string to strip out nasty things like newlines, excess spaces
    Far from prefect at the moment, but gets 80% of the way there.

    Example:

    >>> clean_string("    I am MESSY    ")
    "I am MESSY"
    """
    # Remove all newlines
    string = string.replace('\n', '').replace('\r', '')
    # Remove duplicate spaces.
    string = " ".join(string.split())
    # Remove leading and ending spaces.
    return string.strip()


def truncate_string(string, length, end_text="..."):
    """
    Simple helper function to help truncate long strings.

    Example:

    >>> truncate_string("A long string", 6)
    "A l..."
    """
    if string and len(string) > length:
        return string[:length - len(end_text)] + end_text
    else:
        return string


def strip_html(string):
    """
    Helper function to remove HTML tags and whitespace from a
    given string.

    Example:

    >>> strip_html("<b>  A string  </b>")
    "A string"
    """
    if string:
        soup = BeautifulSoup(string)
        return soup.get_text().strip()
    return string


def strip_all_tags(string):
    """
    Greedily strip all HTML tags and trailing partial tags from a string using
    regex.

    Example:

    >>> string_all_tags("Sorry to interrupt but <a href=")
    "Sorry to interrupt but "
    """
    # Remove all strings that start and end with an angle brace and don't
    # contain any other angle braces
    string = re.sub(r'<[^<>]*?>', "", string)
    # Remove all strings that start with an angle brace followed immediately by
    # a non-whitespace, non-numeric character
    string = re.sub(r'<[^\s0-9].*', "", string)
    # Remove all strings that end with an angle brace preceded immediately by
    # a non-whitespace, non-numeric character
    string = re.sub(r'.*[^\s0-9]>', "", string)
    return string


def remove_words_from_text(text, words):
    """
    Removes a list of words from a text string.

    Example:

    >>> banned = ["don't"]
    >>> text = "I don't like ice cream"
    >>> remove_words_from_text(text, banned)
    "I like ice cream"
    """
    text_list = text.split(' ')
    clean_text = [w for w in text_list if w not in set(words)]
    return ' '.join(clean_text)


def extract_links(text):
    """
    Returns a list of urls present in a body of text.

    Example:

    >>> text = "Fred went to http://google.com"
    >>> extract_links(text)
    ["http://google.com"]
    """
    if not text:
        return []
    regex = re.compile(
        r'(?:(?:http|ftp)s?://)?'  # http:// or https://
        r'(?:(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)?'  # subdomain...
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.))|'  # domain
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)(?:[^\s|^"]+)?', re.IGNORECASE)
    return regex.findall(text)


def extract_hashtags(text):
    """
    Returns a list of hashtags present in a text string

    Example:

    >>> text = "banana #yolo"
    >>> extract_hashtags(text)
    ['#yolo']
    """
    if not text:
        return []
    regex = re.compile(r'#(\w+)')
    hashtags = regex.findall(text)
    return ['#' + h for h in hashtags]


def extract_raw_text(text):
    """
    Removes all links, html and hashtags from a text string.

    Example:

    >>> text = "Check <b>this</b> out! http://yolo.co #yoloco"
    >>> extract_raw_text(text)
    "Check this out!"
    """
    clean_text = strip_all_tags(text)
    extracted_links = extract_links(clean_text)
    extracted_hashtags = extract_hashtags(clean_text)
    return remove_words_from_text(
        clean_text, extracted_links + extracted_hashtags)


def extract_text_from_dict(doc={}, keys=[]):
    """
    Pass in a dict and a list of keys to return a space-separated
    single string of the values in those keys.
    Not appropriate for nested keys.

    Example:

    >>> profile = {"name": "Cam", "favorite_color": "red", "height": "???"}
    >>> extract_text_from_dict(profile, keys=["name", "favorite_color"])
    "Cam red"
    """
    text = []
    for key in keys:
        try:
            if doc[key]:
                text.append(str(doc[key]))
        except:
            continue
    return ' '.join(text)


def humanize_join(items, limit=4, ending='and more'):
    """
    Give a list of items, joins the first ones by comma and last one by and.

    Example:

    >>> names = ['Cam', 'Jon', 'Fred', 'Fletcher']
    >>> humanize_join(names, 1, 'and others.')
    'Cam and others.'
    >>> humanize_join(names, 2)
    'Cam, Jon, and more'
    """
    text = ''
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    elif len(items) > limit:
        text = ", ".join(items[0:limit])
        if limit == 1 or len(items) == 2:
            text = "{} {}".format(text, ending)
        else:
            text = "{}, {}".format(text, ending)
    else:
        text = ", ".join(items[0:-1])
        if limit == 1 or len(items) == 2:
            text = "{} and {}".format(text, items[-1])
        else:
            text = "{}, and {}".format(text, items[-1])
    return text
