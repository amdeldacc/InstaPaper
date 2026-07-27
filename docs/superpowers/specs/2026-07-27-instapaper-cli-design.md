# Instapaper CLI — Design Spec

**Goal:** A Python CLI tool that queries a user's Instapaper account and retrieves stored articles matching a search term.

**Architecture:** Single Python package with Click CLI. Vendored/extended `InstapaperApiClient` from the official example. Client-side search filtering. OAuth 1.0a via xAuth with token caching.

**Tech Stack:** Python 3.10+, Click, requests, requests-oauthlib, toml

## Auth Flow

1. User registers app at instapaper.com/developers → gets consumer_key + consumer_secret
2. First run: `instapaper configure` prompts for email/password → xAuth → OAuth token cached
3. Token stored in `~/.instapaper/config.toml` (chmod 600)
4. Subsequent runs use cached token; if expired, re-prompt for password

## CLI Interface

```
instapaper configure
instapaper search <query> [--folder FOLDER] [--limit N] [--json] [--text N]
```

- `search` — default output: numbered list with title + URL + progress
- `--json` — raw JSON array
- `--text N` — fetch and print full article text for result N
- `--folder` — scope to `unread` (default), `starred`, `archive`, or folder name
- `--limit` — results per page (1-500, default 50)

## Search

Client-side: fetch bookmarks from API → filter by substring/regex match on title, description, URL, tags. No API-level search endpoint.

## Output Formats

**Default:**
```
 1. How to Build X (https://example.com/article) [75%]
 2. Y Patterns Explained (https://example.com/y) [unread]
```

**--json:** Raw JSON array of bookmark objects (with article_text if `--text`).

**--text N:** Full article HTML (from `bookmarks/get_text`), stripped of Instapaper chrome, printed to stdout.

## File Structure

```
instapaper-cli/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── __main__.py        # python -m entrypoint
│   ├── cli.py             # Click commands
│   ├── client.py          # vendored InstapaperApiClient + text fetch
│   ├── config.py          # credential/token read/write
│   └── search.py          # client-side query matching
└── README.md
```

## Data Storage

File: `~/.instapaper/config.toml`
- `consumer_key`, `consumer_secret`, `oauth_token`, `oauth_token_secret`
- chmod 600

## Non-Goals (v1)

- No server-side search
- No add/delete/archive/star operations
- No folder management
- No OAuth token refresh beyond re-auth
