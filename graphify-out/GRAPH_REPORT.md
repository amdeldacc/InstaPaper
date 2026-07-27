# Graph Report - .  (2026-07-27)

## Corpus Check
- Corpus is ~9,991 words - fits in a single context window. You may not need a graph.

## Summary
- 74 nodes · 122 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API Client Layer
- Project Documentation
- CLI Commands
- Config Management
- Search Module
- Agent Workflow
- Package Metadata

## God Nodes (most connected - your core abstractions)
1. `InstapaperClient` - 20 edges
2. `instapaper-cli` - 16 edges
3. `search_bookmarks()` - 9 edges
4. `ai-context skill` - 9 edges
5. `search()` - 6 edges
6. `load()` - 6 edges
7. `requests-oauthlib 1.3+` - 5 edges
8. `pytest` - 5 edges
9. `configure()` - 4 edges
10. `save()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `InstapaperClient` ----> `Instapaper API 1.1`  [EXTRACTED]
  src/client.py → ARCHITECTURE.md
- `InstapaperClient` ----> `OAuth 1.0a / xAuth`  [EXTRACTED]
  src/client.py → ARCHITECTURE.md
- `InstapaperClient` ----> `requests 2.28+`  [EXTRACTED]
  src/client.py → pyproject.toml
- `InstapaperClient` ----> `requests-oauthlib 1.3+`  [EXTRACTED]
  src/client.py → pyproject.toml
- `instapaper-cli` ----> `Click 8.0+`  [EXTRACTED]
  PRD.md → pyproject.toml

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "API Client Layer"
Cohesion: 0.20
Nodes (11): oauth/access_token, bookmarks/get_text, bookmarks/list, folders/list, OAuth1, requests 2.28+, requests-oauthlib 1.3+, InstapaperClient (+3 more)

### Community 1 - "Project Documentation"
Cohesion: 0.23
Nodes (6): Instapaper API 1.1, ai-context skill, graphify, instapaper-cli, setuptools >=64, ~/templates/ai-context/

### Community 2 - "CLI Commands"
Cohesion: 0.20
Nodes (9): OAuth 1.0a / xAuth, Click 8.0+, Client-side substring search, instapaper configure, instapaper search, configure(), main(), Set up API credentials and authenticate. (+1 more)

### Community 3 - "Config Management"
Cohesion: 0.29
Nodes (9): ~/.instapaper/config.toml, Search your Instapaper bookmarks., search(), load(), save(), test_load_nonexistent_config(), test_load_returns_dict(), test_save_and_load_config() (+1 more)

### Community 4 - "Search Module"
Cohesion: 0.31
Nodes (9): pytest, requests_mock, search_bookmarks(), test_case_insensitive(), test_matches_description(), test_matches_tag(), test_matches_title(), test_matches_url() (+1 more)

### Community 5 - "Agent Workflow"
Cohesion: 0.29
Nodes (6): AI Context Files system, caveman skill, rtk (rust token killer), subagent-driven-development, Superpowers skills framework, writing-plans

## Knowledge Gaps
- **13 isolated node(s):** `instapaper-cli`, `requests_mock`, `~/.instapaper/config.toml`, `setuptools >=64`, `~/templates/ai-context/` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `instapaper-cli` connect `Project Documentation` to `API Client Layer`, `CLI Commands`, `Config Management`, `Search Module`, `Agent Workflow`?**
  _High betweenness centrality (0.424) - this node is a cross-community bridge._
- **Why does `InstapaperClient` connect `API Client Layer` to `Project Documentation`, `CLI Commands`, `Config Management`?**
  _High betweenness centrality (0.306) - this node is a cross-community bridge._
- **Why does `pytest` connect `Search Module` to `API Client Layer`, `Project Documentation`, `Config Management`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `InstapaperClient` (e.g. with `configure()` and `search()`) actually correct?**
  _`InstapaperClient` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `OAuth1` (e.g. with `search()` and `test_get_text_returns_none_on_failure()`) actually correct?**
  _`OAuth1` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `instapaper-cli`, `requests_mock`, `~/.instapaper/config.toml` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._