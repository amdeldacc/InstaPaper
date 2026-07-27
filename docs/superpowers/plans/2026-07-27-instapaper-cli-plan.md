# Instapaper CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Python CLI tool that queries Instapaper and retrieves articles matching a search query.

**Architecture:** Single Click CLI package with vendored InstapaperApiClient. xAuth OAuth 1.0a with local token caching. Client-side search filtering.

**Tech Stack:** Python 3.10+, Click, requests, requests-oauthlib, toml

## Global Constraints

- Python 3.10+ only
- Dependencies: click, requests, requests-oauthlib
- Config file: `~/.instapaper/config.toml`, chmod 600
- Use xAuth for OAuth token acquisition
- Search is client-side (titles, descriptions, URLs, tags)
- Folder id mapping: "unread" (default), "starred", "archive", or fetch folder list

---

### Task 1: Project skeleton + config module

**Files:**
- Create: `pyproject.toml`
- Create: `src/__init__.py`
- Create: `src/__main__.py`
- Create: `src/config.py`
- Create: `tests/test_config.py`

**Interfaces:**
- Produces: `config.load() -> dict` / `config.save(data: dict) -> None`
- Produces: `CONFIG_PATH = Path("~/.instapaper/config.toml")`

- [ ] **Step 1: Write project skeleton**

`pyproject.toml`:
```toml
[project]
name = "instapaper-cli"
version = "0.1.0"
description = "CLI tool to search and retrieve Instapaper articles"
requires-python = ">=3.10"
dependencies = [
    "click>=8.0",
    "requests>=2.28",
    "requests-oauthlib>=1.3",
]

[project.scripts]
instapaper = "src.cli:main"

[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.backends._legacy:_Backend"
```

`src/__init__.py`:
```python
```

`src/__main__.py`:
```python
from .cli import main
main()
```

- [ ] **Step 2: Write failing config tests**

`tests/test_config.py`:
```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_config.py -v`
Expected: FAIL — module not found

- [ ] **Step 4: Write config module**

`src/config.py`:
```python
import toml
from pathlib import Path

CONFIG_PATH = Path.home() / ".instapaper" / "config.toml"

def load() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return toml.loads(CONFIG_PATH.read_text())

def save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(toml.dumps(data))
    CONFIG_PATH.chmod(0o600)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_config.py -v`
Expected: 3 PASS

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/__init__.py src/__main__.py src/config.py tests/test_config.py
git commit -m "feat: project skeleton with config module"
```

---

### Task 2: API client (vendored + extended)

**Files:**
- Create: `src/client.py`
- Create: `tests/test_client.py`

**Interfaces:**
- Consumes: `config.load()` from Task 1
- Produces: `InstapaperClient(consumer_key, consumer_secret)`
- Methods: `authenticate(username, password) -> OAuth1 | None`, `list_bookmarks(oauth, folder_id, limit, tag) -> list`, `get_text(oauth, bookmark_id) -> str | None`, `list_folders(oauth) -> list`

- [ ] **Step 1: Write failing tests**

`tests/test_client.py`:
```python
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
```

- [ ] **Step 2: Run to confirm fail**

Run: `pytest tests/test_client.py -v`
Expected: FAIL — import error

- [ ] **Step 3: Write client**

`src/client.py`:
```python
import requests
from requests_oauthlib import OAuth1
import urllib.parse
from typing import Optional

class InstapaperClient:
    BASE_URL = "https://www.instapaper.com/api/1.1"

    def __init__(self, consumer_key: str, consumer_secret: str):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.app_consumer = OAuth1(consumer_key, client_secret=consumer_secret)

    def authenticate(self, username: str, password: str) -> Optional[OAuth1]:
        params = {"x_auth_username": username, "x_auth_password": password}
        r = requests.post(f"{self.BASE_URL}/oauth/access_token", params=params, auth=self.app_consumer)
        if r.status_code != 200:
            return None
        qs = urllib.parse.parse_qs(r.text)
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=qs["oauth_token"][0],
            resource_owner_secret=qs["oauth_token_secret"][0],
        )

    def list_bookmarks(self, oauth: OAuth1, folder_id: str = "unread", limit: int = 50, tag: Optional[str] = None) -> list:
        params = {"format": "json", "folder_id": folder_id, "limit": limit}
        if tag:
            params["tag"] = tag
        r = requests.post(f"{self.BASE_URL}/bookmarks/list", params=params, auth=oauth)
        return r.json() if r.status_code == 200 else []

    def get_text(self, oauth: OAuth1, bookmark_id: int) -> Optional[str]:
        r = requests.post(f"{self.BASE_URL}/bookmarks/get_text", params={"bookmark_id": bookmark_id}, auth=oauth)
        return r.text if r.status_code == 200 else None

    def list_folders(self, oauth: OAuth1) -> list:
        r = requests.post(f"{self.BASE_URL}/folders/list", params={"format": "json"}, auth=oauth)
        return r.json() if r.status_code == 200 else []
```

- [ ] **Step 4: Run tests to pass**

Run: `pytest tests/test_client.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/client.py tests/test_client.py
git commit -m "feat: vendored Instapaper API client with auth, list, get_text, folders"
```

---

### Task 3: Search module

**Files:**
- Create: `src/search.py`
- Create: `tests/test_search.py`

**Interfaces:**
- Consumes: bookmark dicts with keys `title`, `description`, `url`, `tags`
- Produces: `search_bookmarks(bookmarks: list, query: str) -> list`

- [ ] **Step 1: Write failing tests**

`tests/test_search.py`:
```python
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
```

- [ ] **Step 2: Run to confirm fail**

Run: `pytest tests/test_search.py -v`
Expected: FAIL — import error

- [ ] **Step 3: Write search module**

`src/search.py`:
```python
def search_bookmarks(bookmarks: list, query: str) -> list:
    q = query.lower()
    results = []
    for b in bookmarks:
        fields = [
            b.get("title", ""),
            b.get("description", ""),
            b.get("url", ""),
        ]
        fields.extend(t.get("name", "") for t in b.get("tags", []))
        if any(q in f.lower() for f in fields):
            results.append(b)
    return results
```

- [ ] **Step 4: Run tests to pass**

Run: `pytest tests/test_search.py -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add src/search.py tests/test_search.py
git commit -m "feat: client-side bookmark search by title, description, URL, tags"
```

---

### Task 4: CLI module

**Files:**
- Create: `src/cli.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: all modules above
- Produces: `main()` Click entrypoint
- Commands: `configure`, `search`

- [ ] **Step 1: Write failing tests**

`tests/test_cli.py`:
```python
from click.testing import CliRunner
from src.cli import main

def test_search_not_configured():
    runner = CliRunner()
    result = runner.invoke(main, ["search", "test"])
    assert "Not configured" in result.output
    assert result.exit_code != 0
```

- [ ] **Step 2: Run to confirm fail**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL — import error

- [ ] **Step 3: Write CLI module**

`src/cli.py`:
```python
import click
import sys
from .config import load, save
from .client import InstapaperClient
from .search import search_bookmarks
from requests_oauthlib import OAuth1

@click.group()
def main():
    pass

@main.command()
@click.option("--consumer-key", prompt=True, hide_input=False)
@click.option("--consumer-secret", prompt=True, hide_input=False)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def configure(consumer_key, consumer_secret, email, password):
    """Set up API credentials and authenticate."""
    client = InstapaperClient(consumer_key, consumer_secret)
    oauth = client.authenticate(email, password)
    if oauth is None:
        click.echo("Authentication failed", err=True)
        sys.exit(1)
    save({
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
        "oauth_token": oauth.client.resource_owner_key,
        "oauth_token_secret": oauth.client.resource_owner_secret,
    })
    click.echo("Configured successfully")

@main.command()
@click.argument("query")
@click.option("--folder", default="unread", help="Folder scope: unread, starred, archive, or folder name")
@click.option("--limit", default=50, type=int, help="Max results (1-500)")
@click.option("--json", "json_output", is_flag=True, help="Output as raw JSON")
@click.option("--text", "text_index", type=int, default=None, help="Print full article text for result N")
def search(query, folder, limit, json_output, text_index):
    """Search your Instapaper bookmarks."""
    config = load()
    if not config.get("consumer_key"):
        click.echo("Not configured. Run: instapaper configure", err=True)
        sys.exit(1)

    client = InstapaperClient(config["consumer_key"], config["consumer_secret"])
    oauth = OAuth1(
        config["consumer_key"],
        client_secret=config["consumer_secret"],
        resource_owner_key=config["oauth_token"],
        resource_owner_secret=config["oauth_token_secret"],
    )

    if folder not in ("unread", "starred", "archive"):
        folders = client.list_folders(oauth)
        folder_map = {f.get("title", "").lower(): f.get("folder_id") for f in folders if isinstance(f, dict) and f.get("type") == "folder"}
        fid = folder_map.get(folder.lower())
        if fid is None:
            click.echo(f"Folder '{folder}' not found", err=True)
            sys.exit(1)
        folder_id = str(fid)
    else:
        folder_id = folder

    bookmarks = client.list_bookmarks(oauth, folder_id=folder_id, limit=limit)
    bookmark_list = [b for b in bookmarks if isinstance(b, dict) and b.get("type") == "bookmark"]
    results = search_bookmarks(bookmark_list, query)

    if not results:
        click.echo("No matches found")
        return

    if json_output:
        import json
        click.echo(json.dumps(results, indent=2))
        return

    if text_index is not None:
        if text_index < 1 or text_index > len(results):
            click.echo(f"Index out of range (1-{len(results)})", err=True)
            sys.exit(1)
        bm = results[text_index - 1]
        html = client.get_text(oauth, bm["bookmark_id"])
        click.echo(html or "No text available")
        return

    for i, bm in enumerate(results, 1):
        progress = bm.get("progress")
        pct = f"{int(float(progress) * 100)}%" if progress is not None else "unread"
        click.echo(f"{i:>3}. {bm.get('title', 'Untitled')} ({bm.get('url', '')}) [{pct}]")
```

- [ ] **Step 4: Run tests to pass**

Run: `pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/cli.py tests/test_cli.py
git commit -m "feat: CLI with configure and search commands"
```

---

### Task 5: Cleanup + README

**Files:**
- Create: `README.md`
- Create: `.gitignore`

- [ ] **Step 1: Write README**

```markdown
# Instapaper CLI

Query your Instapaper bookmarks from the command line.

## Setup

1. Register an app at https://www.instapaper.com/developers to get a consumer key and secret.
2. Run the configure command:

```
instapaper configure
```

3. Follow the prompts to enter your API credentials, email, and password.

## Usage

```
instapaper search <query> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--folder` | Folder scope: `unread` (default), `starred`, `archive`, or folder name |
| `--limit N` | Max results (1-500, default 50) |
| `--json` | Output as raw JSON |
| `--text N` | Print full article text for result N |

### Examples

```
instapaper search python
instapaper search "machine learning" --folder starred --limit 100
instapaper search cooking --json
instapaper search rust --text 1
```
```

- [ ] **Step 2: Write .gitignore**

```
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
dist/
build/
```

- [ ] **Step 3: Commit**

```bash
git add README.md .gitignore
git commit -m "docs: README and .gitignore"
```

---

### Task 6: End-to-end verification

- [ ] **Step 1: Install locally**

```bash
pip install -e .
```

Expected: package installs without error

- [ ] **Step 2: Run full test suite**

```bash
pytest tests/ -v
```

Expected: all tests PASS

- [ ] **Step 3: Verify help output**

```bash
instapaper --help
instapaper search --help
instapaper configure --help
```

Expected: help text displays without error
