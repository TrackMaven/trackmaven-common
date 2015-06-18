from trackmaven_common.text import (
    humanize_join, strip_all_tags, truncate_string,  remove_words_from_text,
    extract_text_from_dict, extract_links, extract_hashtags, extract_raw_text)


def test_truncate_string():
    """Test truncate_string correctly shortens strings"""
    long_string = "A long string that needs to be truncate"
    short_string = "Shorty"

    assert truncate_string(long_string, 12) == "A long st..."
    assert truncate_string(long_string, 12, "- The End") == "A l- The End"
    assert truncate_string(short_string, 30) == "Shorty"
    assert truncate_string(None, 30) is None


def test_humanize_join():
    """Test truncate_string correctly shortens strings"""
    names = ['Cam', 'Jon', 'Fred', 'Fletcher', 'Matt', 'Josh', 'John']

    assert humanize_join(names, 3, 'and others.') == 'Cam, Jon, Fred, and others.'
    assert humanize_join(names, 1, 'and others.') == 'Cam and others.'
    assert humanize_join(names, 3) == 'Cam, Jon, Fred, and more'
    assert humanize_join(names, 2) == 'Cam, Jon, and more'
    assert humanize_join(names, 1) == 'Cam and more'
    assert humanize_join(names[0:1], 3) == 'Cam'
    assert humanize_join(names[0:2], 3) == 'Cam and Jon'
    assert humanize_join(names[0:3], 3) == 'Cam, Jon, and Fred'
    assert humanize_join([]) == ''


def test_strip_all_tags():
    """
    Test that strip_all_tags correctly removes complete HTML elements,
    but leaves individual angle brackets intact.
    """
    html_string = "I'm a string with a > and a < in it.<a href='also.an/html/element'></a>"
    cleaned_string = strip_all_tags(html_string)
    assert "I'm a string with a > and a < in it." == cleaned_string


def test_strip_all_tags_trailing_partial():
    """
    Test that strip_all_tags correctly removes trailing partial HTML
    elements.
    """
    html_string = "Sorry to interrupt but <a href="
    cleaned_string = strip_all_tags(html_string)
    assert "Sorry to interrupt but " == cleaned_string


def test_strip_all_tags_leading_partial():
    """
    Test that strip_all_tags correctly removes leading partial HTML
    elements.
    """
    html_string = "/> as I was saying."
    cleaned_string = strip_all_tags(html_string)
    assert " as I was saying." == cleaned_string


def test_strip_all_tags_inequality():
    """
    Test that strip_all_tags preserves numerical inequalities e.g 2<3.
    """
    html_string = "I <3 you"
    cleaned_string = strip_all_tags(html_string)
    assert html_string == cleaned_string


def test_extract_text_from_dict():
    """
    Test that extract text will return only the text from the keys
    specified of the passed-in dict
    """
    test_doc = {'a': 'monkey dishwasher', 'b': 'banana', 'd': None}
    assert extract_text_from_dict(test_doc, keys=['a', 'b', 'c', 'd']) == 'monkey dishwasher banana'


def test_extract_links():
    """
    Test that the regular expression is correctli returning a space-
    delimited string of links found within the original text.
    """
    text = '#banana banana banana #pineapple whooooo! http://www.gooogle.com#monkeydishwasher myspace.com/instapics'
    expected = ['http://www.gooogle.com#monkeydishwasher', 'myspace.com/instapics']
    assert expected == extract_links(text)


def test_extract_links_multiple():
    """
    Test that the regular expression is correctly returning a space-
    delimited string of links found within the original text.
    """
    text = '#banana banana http://google.com banana #pineapple whooooo! http://www.gooogle.com#monkeydishwasher'
    expected = ['http://google.com', 'http://www.gooogle.com#monkeydishwasher']
    assert expected == extract_links(text)


def test_extract_links_html():
    """
    Get a link out of some HTML
    """
    text = '#banana is #apple my kind of tic tac toe <a href="http://pinterest.com/search?q=zappos" target="_blank">#zappos</a>'
    expected = ['http://pinterest.com/search?q=zappos']
    assert expected == extract_links(text)


def test_extract_hashtags():
    """
    Tests extracting hashtags from text string.
    """
    text = "this is a #hashtag"
    assert ['#hashtag'] == extract_hashtags(text)


def test_remove_words_from_text():
    """
    Tests extracting items from a text string.
    """
    items_to_remove = ['#yolo', 'http://www.google.com']
    text = 'wow #yolo http://www.google.com'
    assert 'wow' == remove_words_from_text(text, items_to_remove)


def test_extract_raw_text():
    """
    Tests extracting raw text (no html, links or hashtags) from a text
    string.
    """
    text = "<b>This</b> is #awesome http://goog.co www.google.com"
    assert 'This is' == extract_raw_text(text)
