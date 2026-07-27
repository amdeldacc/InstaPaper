# Phases — Implementation Plan

<!-- Updated by ai-context skill on 2026-07-27. -->

## Phase 1: Core CLI (Done)

**Scope:** Configure, search, client-side filtering, basic output.

**Dependencies:** None.

**Done Criteria:**
- [x] `instapaper configure` prompts for credentials and caches them
- [x] `instapaper search <query>` searches by title/description/URL/tags
- [x] `--folder`, `--limit`, `--json`, `--text N` options work
- [x] `--fetch-all` paginates across all bookmarks (500 per page)
- [x] `--deep` searches inside full article body text
- [x] Warning on empty API response mid-pagination
- [x] All tests pass with requests_mock (no live API calls)
- [x] Package installs via pip

---

## Phase 2: Polish & Error Handling

**Scope:** Improve error messages, edge cases, input validation.

**Dependencies:** Phase 1 complete

**Done Criteria:**
- [ ] Graceful handling of network timeouts and API errors
- [ ] Better error messages for invalid --limit values
- [ ] Handle special characters in search queries

---

## Phase 3: Additional API Features (Optional)

**Scope:** More Instapaper API endpoints.

**Dependencies:** Phase 1 complete

**Done Criteria:**
- [ ] `instapaper list --folder <folder>` — list bookmarks without search filter
- [ ] `instapaper folders` — list and display folders
- [ ] `instapaper stats` — show bookmark count, unread count

---

## Phase 4: Integrations (Optional)

**Scope:** Pipe into other tools.

**Dependencies:** Phase 1 complete

**Done Criteria:**
- [ ] `--format csv` for spreadsheet import
- [ ] `--format url-only` for piping into browser/bookmark tools
- [ ] Support for `~/.instapaper/config.toml` env var overrides

---

## Phase 5: Testing & Cleanup

**Scope:** Hardening.

**Dependencies:** Phase 1 complete (Phase 2 optional)

**Done Criteria:**
- [ ] Test coverage > 85%
- [ ] Edge cases documented in TESTING.md
- [ ] Performance benchmarks for large bookmark sets
