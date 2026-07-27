import pytest
from pathlib import Path
from src.config import save, load, CONFIG_PATH

def test_save_and_load_config(tmp_path, monkeypatch):
    monkeypatch.setattr("src.config.CONFIG_PATH", tmp_path / "config.toml")
    data = {"consumer_key": "ck", "consumer_secret": "cs"}
    save(data)
    loaded = load()
    assert loaded == data

def test_load_nonexistent_config(tmp_path, monkeypatch):
    monkeypatch.setattr("src.config.CONFIG_PATH", tmp_path / "nope.toml")
    loaded = load()
    assert loaded == {}

def test_load_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr("src.config.CONFIG_PATH", tmp_path / "config.toml")
    result = load()
    assert isinstance(result, dict)
