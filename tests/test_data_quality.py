import pytest
from src.data_quality import validate_article, filter_articles

def test_validate_article_good():
    good = {'title': 'Valid Title', 'url': 'http://example.com', 'publishedAt': '2024-01-01'}
    assert validate_article(good) is True

def test_validate_article_bad():
    bad = {'title': '', 'url': None, 'publishedAt': ''}
    assert validate_article(bad) is False

def test_filter_articles():
    articles = [
        {'title': 'Good Title', 'url': 'http://a.com', 'publishedAt': '2024-01-01'},  # length >=5
        {'title': '', 'url': 'http://b.com', 'publishedAt': '2024-01-02'},           # empty title
        {'title': 'Another', 'url': None, 'publishedAt': '2024-01-03'},              # None URL
    ]
    filtered = filter_articles(articles)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'Good Title'