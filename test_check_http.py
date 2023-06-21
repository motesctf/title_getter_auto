import pytest
from title_getter import check_http


def test_with_http():
    url = "http://example.com"
    result = check_http(url)
    assert result == url


def test_with_https():
    url = "https://example.com"
    result = check_http(url)
    assert result == url


def test_with_domain():
    url = "example.com"
    result = check_http(url)
    assert result == "http://" + url

