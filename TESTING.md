# Testing — Guide

<!-- Updated by ai-context skill on 2026-07-27. -->

## Testing Strategy

- **Unit tests**: pytest for all modules under `src/`
- **Integration tests**: API calls mocked with requests_mock (no live HTTP)
- **CLI tests**: Click CliRunner for end-to-end command invocation
- **Coverage target**: 85%+ (focus on search logic and CLI edge cases)

## Critical Flows to Test

1. Config save/load with valid and missing files
2. Client auth — successful and failed xAuth exchange
3. Client list_bookmarks — with and without folder/tag filters
4. Client get_text — success and 400 response
5. Client list_folders — normal and empty response
6. Search matching — title, description, URL, tags, case-insensitive, no-match
7. Body search with `--deep` — body match, body no-match, case-insensitive, missing bookmark_id, bodies=None
8. CLI `configure` — happy path and auth failure
9. CLI `search` — unconfigured error, results, no results, --json, --text, --folder, --limit
10. Pagination — `--fetch-all`, multiple pages, empty mid-page warning

## Edge Cases

- Config file with missing keys
- Bookmarks list containing non-dict entries
- Malformed HTML from `get_text` (just pass through)
- Folder name not found in folder list
- `--limit` values outside 1–500 range (handled by API)
- `--text N` with N out of range
- Search query with special regex characters (substring match, not regex)

## Validation Rules

- Consumer key/secret must be non-empty strings
- Email/password must be non-empty
- Search query must be non-empty string
- --limit must be integer 1–500 (Click handles this)
- --text must be positive integer
- --folder defaults to "unread" if unspecified

## Pre-Release Checklist

- [ ] `pytest tests/ -v` — all tests pass
- [ ] `pip install -e .` — installs without error
- [ ] `instapaper --help` — displays help text
- [ ] `instapaper search --help` — displays search help
- [ ] `instapaper configure --help` — displays configure help
