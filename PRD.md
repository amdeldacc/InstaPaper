# PRD — Product Requirements Document

<!-- Updated by ai-context skill on 2026-07-27. -->

## Problem

Instapaper users accumulate hundreds or thousands of bookmarked articles. The official Instapaper app and website offer limited search — no CLI access, no programmatic querying, no integration with developer workflows. Users who want to find a specific article in their archive must scroll through pages or use fuzzy memory.

## Target Users

- **Developers** who use Instapaper and want to search bookmarks from the terminal
- **Power users** who integrate bookmark search into scripts, pipelines, or automation
- **Anyone** who prefers keyboard-driven workflows over GUI navigation

## Core Features

- OAuth 1.0a (xAuth) authentication with token caching
- Search bookmarks by substring match on title, description, URL, and tags
- Deep search inside full article body text (--deep, 1 HTTP req/article)
- Paginate across all bookmarks (--fetch-all, pages of 500)
- Filter by folder: unread, starred, archive, or named folders
- Fetch full article text for any result
- Configurable result limits (1–500)
- JSON output for piping into other tools (jq, scripts)

## User Roles / Personas

- **End User**: Runs `instapaper search <query>` to find articles. No programming required.
- **Power User**: Uses `--json` to pipe results into scripts, or `--text` to extract article content.

## Functional Requirements

1. Users can authenticate via `instapaper configure` with consumer key/secret + email/password
2. Credentials and OAuth tokens are cached in `~/.instapaper/config.toml` (chmod 600)
3. Users can search bookmarks with `instapaper search <query>`
4. Search matches on title, description, URL, and tag name (case-insensitive)
5. Users can scope search to a folder with `--folder`
6. Users can limit results with `--limit N` (1–500, default 50)
7. Users can output as JSON with `--json`
8. Users can fetch full article text for a result with `--text N`
9. Users can paginate across all bookmarks with `--fetch-all` (500 per page)
10. Users can search inside article body text with `--deep`
11. Pagination warns on empty response mid-stream
12. Invalid folder names produce a clear error message
13. Unconfigured state produces "Not configured" message and non-zero exit code

## Non-Functional Requirements

- CLI response time dominated by Instapaper API latency (< 1s local processing)
- No data stored server-side — all search is client-side
- Credentials file readable only by the owning user (chmod 600)
- Python 3.10+ only, minimal dependencies: click, requests, requests-oauthlib, toml

## Success Criteria

- [ ] `instapaper configure` completes auth in < 3 interactive prompts
- [ ] `instapaper search <query>` returns matching results from a configured account
- [ ] All existing tests pass without live API calls (requests_mock)
- [ ] Package installs with `pip install -e .`

## Out of Scope

- Server-side search (Instapaper API has no search endpoint)
- Adding, deleting, archiving, or starring bookmarks
- Folder management (create/rename/delete folders)
- OAuth token refresh — re-auth via password on expiry
- Web UI or GUI
- Mobile app or browser extension
