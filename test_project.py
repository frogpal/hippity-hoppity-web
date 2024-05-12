import pytest
from project import get_basename, get_css, get_soup, get_title
from bs4 import BeautifulSoup
from urllib.error import URLError


def test_get_soup():
    soup_object = get_soup("https://markmanson.net/question")
    assert isinstance(soup_object, BeautifulSoup)
    with pytest.raises(URLError):
        assert get_soup("https://www.iundiugntfih.com")
    with pytest.raises(ValueError):
        assert get_soup("invalid url")


def test_get_basename():
    assert get_basename("my_font.woff2?query_params#something") == "my_font.woff2"
    assert get_basename("image.png#something") == "image.png"
    assert get_basename("test.svg?query") == "test.svg"


def test_get_title():
    assert (
        get_title(get_soup("https://en.wikipedia.org/wiki/D-subminiature"))
        == "d-subminiature-wikipedia"
    )
    assert get_title(get_soup("https://www.harvard.edu/")) == "harvard-university"


def test_get_css():
    assert isinstance(get_css("https://realpython.com/"), str)
    assert isinstance(
        get_css("https://beautiful-soup-4.readthedocs.io/en/latest/"), str
    )
