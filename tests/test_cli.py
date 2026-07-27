from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.cli import main

CONFIG = {"consumer_key": "ck", "consumer_secret": "cs", "oauth_token": "ot", "oauth_token_secret": "os"}

def test_search_not_configured():
    runner = CliRunner()
    with patch("src.cli.load", return_value={}):
        result = runner.invoke(main, ["search", "test"])
    assert "Not configured" in result.output
    assert result.exit_code != 0

def test_fetch_all_paginates():
    page1 = [{"bookmark_id": i, "title": f"T{i}", "url": f"http://a.com/{i}", "type": "bookmark"} for i in range(500)]
    with (
        patch("src.cli.load", return_value=CONFIG),
        patch("src.cli.InstapaperClient.list_bookmarks",
              side_effect=[
                  page1,
                  [{"bookmark_id": 500, "title": "Alpha", "url": "http://a.com/500", "type": "bookmark"}],
                  [],
              ]),
        patch("src.cli.OAuth1"),
    ):
        runner = CliRunner()
        result = runner.invoke(main, ["search", "Alpha", "--fetch-all"])
    assert result.exit_code == 0
    assert "Alpha" in result.output

def test_fetch_all_warns_on_mid_pagination_empty():
    page1 = [{"bookmark_id": i, "title": f"T{i}", "url": f"http://a.com/{i}", "type": "bookmark"} for i in range(500)]
    with (
        patch("src.cli.load", return_value=CONFIG),
        patch("src.cli.InstapaperClient.list_bookmarks",
              side_effect=[
                  page1,
                  [],
              ]),
        patch("src.cli.OAuth1"),
    ):
        runner = CliRunner()
        result = runner.invoke(main, ["search", "T0", "--fetch-all"])
    assert "Warning" in result.output
    assert "T0" in result.output

def test_deep_search():
    with (
        patch("src.cli.load", return_value=CONFIG),
        patch("src.cli.InstapaperClient.list_bookmarks",
              return_value=[{"bookmark_id": 1, "title": "Title", "url": "http://a.com", "type": "bookmark"}]),
        patch("src.cli.InstapaperClient.get_text", return_value="hidden quantum content"),
        patch("src.cli.OAuth1"),
    ):
        runner = CliRunner()
        result = runner.invoke(main, ["search", "quantum", "--deep"])
    assert result.exit_code == 0
    assert "Title" in result.output

def test_deep_search_no_body_match():
    with (
        patch("src.cli.load", return_value=CONFIG),
        patch("src.cli.InstapaperClient.list_bookmarks",
              return_value=[{"bookmark_id": 1, "title": "Title", "url": "http://a.com", "type": "bookmark"}]),
        patch("src.cli.InstapaperClient.get_text", return_value="nothing relevant"),
        patch("src.cli.OAuth1"),
    ):
        runner = CliRunner()
        result = runner.invoke(main, ["search", "quantum", "--deep"])
    assert "No matches" in result.output
