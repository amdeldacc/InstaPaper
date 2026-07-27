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
