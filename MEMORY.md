# Memory — Project State

<!-- Updated by ai-context skill on 2026-07-27. -->

## What's Done

- [x] Project skeleton with pyproject.toml and package structure (2026-07-27)
- [x] Config module — read/write `~/.instapaper/config.toml` with chmod 600 (2026-07-27)
- [x] Vendored InstapaperApiClient — xAuth auth, list bookmarks, get_text, list folders (2026-07-27)
- [x] Client-side search module — substring match on title/description/URL/tags (2026-07-27)
- [x] CLI module — `configure` and `search` commands with all options (2026-07-27)
- [x] `--fetch-all` pagination across all bookmarks (500 per page, 2026-07-27)
- [x] `--deep` search inside full article body text (2026-07-27)
- [x] `offset` parameter on `list_bookmarks()` for pagination (2026-07-27)
- [x] Mid-pagination warning on empty API response (2026-07-27)
- [x] Fixed double `r.json()` call in `list_bookmarks()` (2026-07-27)
- [x] Full test suite — 23 tests with requests_mock (2026-07-27)
- [x] AI context files — PRD, ARCHITECTURE, RULES, PHASES, TESTING, DECISIONS, MEMORY (2026-07-27)

## Current Phase

**Phase 1: Core CLI** — Done

## Active Work

- [ ] None — Phase 1 complete, awaiting Phase 2

## Key Decisions

- **2026-07-27**: Chose client-side substring search because Instapaper API has no search endpoint
- **2026-07-27**: Chose xAuth over full OAuth because Instapaper supports only xAuth for CLI apps
- **2026-07-27**: Chose vendored client over external package to keep dependency surface minimal
- **2026-07-27**: Chose TOML for config because Instapaper uses TOML natively

## Known Issues

- `bookmarks/get_text` may require Instaparser API key for non-personal use
- No retry logic for transient API failures
- OAuth tokens may expire without warning; re-run `configure`
- `--deep` is slow on large libraries (sequential HTTP, 1 req/article)
- `*.md` in `.gitignore` ignores all markdown files broadly

## Open Tasks

- [ ] Phase 2: Polish error handling and edge cases
- [ ] Phase 3: Additional API features (list, folders, stats)

## Next Step

- [ ] Run full test suite: `pytest tests/ -v`
