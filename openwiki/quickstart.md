---
type: Quickstart
title: Instapaper CLI Quickstart
description: Entry point for the Instapaper CLI wiki — setup, usage, architecture overview, and navigation to all docs.
resource: https://github.com/piou/InstaPaper
tags: [quickstart, overview, cli, instapaper]
---

# Instapaper CLI — Quickstart

A Python CLI to search and retrieve your Instapaper bookmarks from the command line.

## What This Wiki Covers

This single-page wiki is the entry point. Deeper pages (architecture overview, source map, workflows, domain concepts, operations runbook, testing guidance, integration notes) are listed in the [Backlog](#backlog) and will be promoted as the codebase grows.

## Quick Setup

```bash
# 1. Install
pip install -e .

# 2. Register an app at https://www.instapaper.com/developers
#    Get your consumer key and secret

# 3. Configure
instapaper configure
# Enter: consumer key, consumer secret, email, password
```

## Quick Usage

```bash
# Search unread bookmarks (default)
instapaper search python

# Search starred folder, limit 100
instapaper search "machine learning" --folder starred --limit 100

# Output JSON
instapaper search cooking --json

# Fetch full article text for result #1
instapaper search rust --text 1

# Search all folders, fetch all pages, deep search article text
instapaper search rust --folder all --fetch-all --deep
```

## Key Options

| Flag | Description |
|------|-------------|
| `--folder` | Folder scope: `unread` (default), `starred`, `archive`, or custom folder name |
| `--limit N` | Max results per page (1–500, default 50) |
| `--fetch-all` | Fetch all pages via `offset` pagination (overrides `--limit` to 500/page) |
| `--deep` | Fetch full article text for each result (1 API call/result); cached bodies are reused by `--text N` without a second round-trip |
| `--json` | Output raw JSON |
| `--text N` | Print full article text for result N (reuses `--deep` cache when available) |

## Architecture at a Glance

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    Terminal --> CLI[src/cli.py<br/>Click group]
    CLI -->|load| Config[~/.instapaper/config.toml]
    CLI -->|list_bookmarks / get_text| Client[src/client.py<br/>InstapaperClient]
    Client -->|OAuth 1.0a xAuth + HTTPS| API[(api.instapaper.com/1.1)]
    CLI -->|search_bookmarks| Search[src/search.py<br/>client-side match]
    Search --> Results[CLI output / JSON / --text]
```

- **Entry**: `src/cli.py` — Click group with `configure` and `search` commands
- **Config**: `src/config.py` — TOML at `~/.instapaper/config.toml` (chmod 600)
- **Client**: `src/client.py` — `InstapaperClient` (OAuth 1.0a xAuth; `list_bookmarks` accepts `offset` and unwraps the `{"bookmarks": [...]}` response envelope)
- **Search**: `src/search.py` — Client-side substring match (no API search endpoint); accepts an optional `bodies` dict for `--deep` article-text search
- **Pagination**: `--fetch-all` loops `list_bookmarks` with `offset=0,500,1000,…` until a short page is returned

## Key Concepts

- **No API search**: Instapaper API has no search endpoint → client fetches bookmarks then filters locally
- **xAuth**: Email/password exchange for OAuth tokens (no browser redirect)
- **Folders**: `unread`, `starred`, `archive`, or custom folder names
- **Deep search**: `--deep` fetches full article text via `bookmarks/get_text` (1 API call per result)

## Next Steps

- Read the source: [`src/cli.py`](/src/cli.py), [`src/client.py`](/src/client.py), [`src/search.py`](/src/search.py), [`src/config.py`](/src/config.py)
- Re-run the suite: `pytest tests/`
- Promote pages from the [Backlog](#backlog) below as the codebase grows

## Backlog

Deeper pages are deferred until the next init/update. Each is grounded in a real source area:

- `architecture/overview.md` — system components and data flow (`src/cli.py`, `src/client.py`)
- `architecture/source-map.md` — file-by-file map (`src/`, `tests/`)
- `workflows/key-workflows.md` — `configure` and `search` end-to-end flows
- `domain/concepts.md` — Instapaper API, xAuth, folders, envelopes, pagination
- `operations/runbook.md` — config location (`~/.instapaper/config.toml`), auth troubleshooting
- `testing/guidance.md` — `tests/test_cli.py`, `tests/test_client.py`, `tests/test_config.py`, `tests/test_search.py`
- `integrations/instapaper-api.md` — endpoints (`/bookmarks/list`, `/bookmarks/get_text`, `/folders/list`, `/oauth/access_token`) and rate limits