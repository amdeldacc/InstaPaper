# instapaper-cli

Search and retrieve your [Instapaper](https://www.instapaper.com) bookmarks from the command line.

Client-side substring matching with no server-side search — uses the Instapaper API to fetch bookmarks, then filters locally.

## Quick start

```bash
pip install -e .
```

Register an app at [instapaper.com/developers](https://www.instapaper.com/developers), then:

```bash
instapaper configure
```

Prompts for consumer key, consumer secret, email, and password. Credentials are stored in `~/.instapaper/config.toml` (chmod 600).

## Usage

```bash
instapaper search <query> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--folder` | `unread` | Folder scope: `unread`, `starred`, `archive`, or custom folder name |
| `--limit` | 50 | Max results per page (1–500) |
| `--fetch-all` | — | Paginate all pages (overrides `--limit` to 500) |
| `--deep` | — | Search article body text (1 HTTP request per article) |
| `--json` | — | Output raw JSON |
| `--text N` | — | Print full article text for result N |

### Examples

```bash
instapaper search python
instapaper search "machine learning" --folder starred --limit 100
instapaper search rust --folder all --fetch-all --deep
instapaper search cooking --json
instapaper search rust --text 1
```

## Architecture

```
┌──────────┐  configure/search  ┌───────────┐  OAuth 1.0a xAuth  ┌──────────────┐
│ Terminal │ ─────────────────▶│  cli.py    │ ──────────────────▶│  Instapape r │
│          │                    │  (Click)  │                    │  API 1.1     │
└──────────┘                    └───────────┘                    └──────────────┘
                                     │
                                     │ search_bookmarks()
                                     ▼
                               ┌───────────┐
                               │ search.py │  local substring match
                               └───────────┘
```

- `src/cli.py` — Click command group (`configure`, `search`)
- `src/client.py` — `InstapaperClient` wrapping OAuth 1.0a xAuth and API calls
- `src/search.py` — `search_bookmarks()` client-side substring match
- `src/config.py` — TOML read/write at `~/.instapaper/config.toml`

The Instapaper API has no search endpoint — the tool fetches bookmarks and filters locally. `--deep` fetches article bodies via `bookmarks/get_text` (1 request per article). `--fetch-all` paginates with `offset=0,500,1000...`.

## Development

```bash
pip install -e .
pytest tests/ -v
```

Tests mock all HTTP calls using `requests_mock` or `unittest.patch`. No live Instapaper account needed.

### CI

Four GitHub Actions workflows:

- **Python application** — `pytest` + `flake8` on push/PR to `main`
- **Pylint** — `pylint --exit-zero` on every push
- **Bandit** — security scan on push/PR to `main` + weekly cron
- **OpenWiki** — daily `openwiki code --update --print` PR generation

All lint workflows use `--exit-zero` — warnings surface without blocking merges.
