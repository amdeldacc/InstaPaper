# Graph Report - /home/piou/InstaPaper  (2026-07-27)

## Corpus Check
- Corpus is ~8,222 words - fits in a single context window. You may not need a graph.

## Summary
- 81 nodes · 119 edges · 9 communities (7 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- CLI Architecture & Design
- Client & OAuth Auth
- Search & Tests
- AI Context Files
- CLI Entrypoint & Integration
- Config & Setup
- OpenWiki Docs
- Package Definition

## God Nodes (most connected - your core abstractions)
1. `search_bookmarks()` - 14 edges
2. `InstapaperClient` - 13 edges
3. `AI Context Files` - 9 edges
4. `main()` - 7 edges
5. `Instapaper CLI Quickstart` - 7 edges
6. `search()` - 6 edges
7. `load()` - 6 edges
8. `Instapaper CLI` - 6 edges
9. `configure()` - 4 edges
10. `save()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `test_deep_search()` --indirect_call--> `main()`  [INFERRED]
  tests/test_cli.py → src/cli.py
- `test_deep_search_no_body_match()` --indirect_call--> `main()`  [INFERRED]
  tests/test_cli.py → src/cli.py
- `test_fetch_all_paginates()` --indirect_call--> `main()`  [INFERRED]
  tests/test_cli.py → src/cli.py
- `test_fetch_all_warns_on_mid_pagination_empty()` --indirect_call--> `main()`  [INFERRED]
  tests/test_cli.py → src/cli.py
- `test_search_not_configured()` --indirect_call--> `main()`  [INFERRED]
  tests/test_cli.py → src/cli.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **CI/CD Pipeline** — github_workflows_bandit_bandit_workflow, github_workflows_openwiki_update_openwiki_workflow, github_workflows_pylint_pylint_workflow, github_workflows_python_app_python_app_workflow [INFERRED 0.95]
- **AI Context Files System** — docs_superpowers_plans_2026_07_27_ai_context_files_plan_ai_context_files, docs_superpowers_plans_2026_07_27_ai_context_files_plan_prd_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_architecture_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_rules_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_phases_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_design_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_memory_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_testing_template, docs_superpowers_plans_2026_07_27_ai_context_files_plan_decisions_template [EXTRACTED 1.00]
- **Instapaper CLI Package** — docs_superpowers_plans_2026_07_27_instapaper_cli_plan_instapaper_cli, docs_superpowers_plans_2026_07_27_instapaper_cli_plan_config_module, docs_superpowers_plans_2026_07_27_instapaper_cli_plan_client_module, docs_superpowers_plans_2026_07_27_instapaper_cli_plan_search_module, docs_superpowers_plans_2026_07_27_instapaper_cli_plan_cli_module [EXTRACTED 1.00]

## Communities (9 total, 2 thin omitted)

### Community 0 - "CLI Architecture & Design"
Cohesion: 0.11
Nodes (20): CLI Module (src/cli.py), InstapaperClient Module (src/client.py), Config Module (src/config.py), Instapaper CLI, Search Module (src/search.py), Client-side Search Pattern, Instapaper CLI Design Spec, OAuth 1.0a xAuth Flow (+12 more)

### Community 1 - "Client & OAuth Auth"
Cohesion: 0.26
Nodes (8): OAuth1, Search your Instapaper bookmarks., search(), InstapaperClient, test_client_initialization(), test_get_text_returns_none_on_failure(), test_list_bookmarks_with_offset(), test_list_folders_returns_list()

### Community 2 - "Search & Tests"
Cohesion: 0.27
Nodes (12): search_bookmarks(), test_case_insensitive(), test_matches_description(), test_matches_tag(), test_matches_title(), test_matches_url(), test_no_match(), test_search_body_case_insensitive() (+4 more)

### Community 3 - "AI Context Files"
Cohesion: 0.18
Nodes (11): AI Context Files, ARCHITECTURE.md Template, DECISIONS.md Template, DESIGN.md Template, MEMORY.md Template, PHASES.md Template, PRD.md Template, RULES.md Template (+3 more)

### Community 4 - "CLI Entrypoint & Integration"
Cohesion: 0.39
Nodes (6): main(), test_deep_search(), test_deep_search_no_body_match(), test_fetch_all_paginates(), test_fetch_all_warns_on_mid_pagination_empty(), test_search_not_configured()

### Community 5 - "Config & Setup"
Cohesion: 0.39
Nodes (7): configure(), Set up API credentials and authenticate., load(), save(), test_load_nonexistent_config(), test_load_returns_dict(), test_save_and_load_config()

## Knowledge Gaps
- **19 isolated node(s):** `instapaper-cli`, `Bandit Security Scanner`, `OpenWiki Documentation Generator`, `Pylint Linter`, `Flake8 Linter` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `search()` connect `Client & OAuth Auth` to `Search & Tests`, `CLI Entrypoint & Integration`, `Config & Setup`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `search_bookmarks()` connect `Search & Tests` to `Client & OAuth Auth`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `InstapaperClient` connect `Client & OAuth Auth` to `Config & Setup`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `InstapaperClient` (e.g. with `configure()` and `search()`) actually correct?**
  _`InstapaperClient` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `OAuth1` (e.g. with `search()` and `test_get_text_returns_none_on_failure()`) actually correct?**
  _`OAuth1` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `main()` (e.g. with `test_deep_search()` and `test_deep_search_no_body_match()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `instapaper-cli`, `Bandit Security Scanner`, `OpenWiki Documentation Generator` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._