import pytest
from requests_oauthlib import OAuth1
from src.client import InstapaperClient

def test_client_initialization():
    client = InstapaperClient("test_key", "test_secret")
    assert client.consumer_key == "test_key"
    assert client.consumer_secret == "test_secret"

def test_get_text_returns_none_on_failure(requests_mock):
    requests_mock.post("https://www.instapaper.com/api/1.1/bookmarks/get_text", status_code=400)
    client = InstapaperClient("k", "s")
    oauth = OAuth1("k", client_secret="s")
    result = client.get_text(oauth, 123)
    assert result is None

def test_list_folders_returns_list(requests_mock):
    requests_mock.post("https://www.instapaper.com/api/1.1/folders/list", json=[{"type": "folder", "folder_id": 1, "title": "Test"}])
    client = InstapaperClient("k", "s")
    oauth = OAuth1("k", client_secret="s")
    result = client.list_folders(oauth)
    assert isinstance(result, list)
