import pytest
from src.search import search_bookmarks

BOOKMARKS = [
    {"bookmark_id": 1, "title": "Python Tips", "description": "cool python tricks", "url": "https://a.com", "tags": [{"name": "code"}]},
    {"bookmark_id": 2, "title": "Rust Guide", "description": "systems programming", "url": "https://b.com", "tags": []},
    {"bookmark_id": 3, "title": "Cooking 101", "description": "how to cook", "url": "https://c.com/python", "tags": [{"name": "food"}]},
]

def test_matches_title():
    assert len(search_bookmarks(BOOKMARKS, "python")) == 2

def test_matches_description():
    assert len(search_bookmarks(BOOKMARKS, "systems")) == 1

def test_matches_url():
    assert len(search_bookmarks(BOOKMARKS, "c.com")) == 1

def test_matches_tag():
    assert len(search_bookmarks(BOOKMARKS, "food")) == 1

def test_no_match():
    assert search_bookmarks(BOOKMARKS, "zzzzz") == []

def test_case_insensitive():
    assert len(search_bookmarks(BOOKMARKS, "PYTHON")) == 2
