import click
import sys
from config import load, save
from client import InstapaperClient
from search import search_bookmarks
from requests_oauthlib import OAuth1

@click.group()
def main():
    pass

@main.command()
@click.option("--consumer-key", prompt=True, hide_input=False)
@click.option("--consumer-secret", prompt=True, hide_input=False)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def configure(consumer_key, consumer_secret, email, password):
    """Set up API credentials and authenticate."""
    client = InstapaperClient(consumer_key, consumer_secret)
    oauth = client.authenticate(email, password)
    if oauth is None:
        click.echo("Authentication failed", err=True)
        sys.exit(1)
    save({
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
        "oauth_token": oauth.client.resource_owner_key,
        "oauth_token_secret": oauth.client.resource_owner_secret,
    })
    click.echo("Configured successfully")

@main.command()
@click.argument("query")
@click.option("--folder", default="unread", help="Folder scope: unread, starred, archive, or folder name")
@click.option("--limit", default=50, type=int, help="Max results per page (1-500)")
@click.option("--fetch-all", is_flag=True, help="Fetch all pages (overrides --limit to 500)")
@click.option("--deep", is_flag=True, help="Also search inside full article text (1 req/article)")
@click.option("--json", "json_output", is_flag=True, help="Output as raw JSON")
@click.option("--text", "text_index", type=int, default=None, help="Print full article text for result N")
def search(query, folder, limit, json_output, text_index, fetch_all, deep):
    """Search your Instapaper bookmarks."""
    config = load()
    if not config.get("consumer_key"):
        click.echo("Not configured. Run: instapaper configure", err=True)
        sys.exit(1)

    client = InstapaperClient(config["consumer_key"], config["consumer_secret"])
    oauth = OAuth1(
        config["consumer_key"],
        client_secret=config["consumer_secret"],
        resource_owner_key=config["oauth_token"],
        resource_owner_secret=config["oauth_token_secret"],
    )

    if folder not in ("unread", "starred", "archive"):
        folders = client.list_folders(oauth)
        folder_map = {f.get("title", "").lower(): f.get("folder_id") for f in folders if isinstance(f, dict) and f.get("type") == "folder"}
        fid = folder_map.get(folder.lower())
        if fid is None:
            click.echo(f"Folder '{folder}' not found", err=True)
            sys.exit(1)
        folder_id = str(fid)
    else:
        folder_id = folder

    page_size = 500 if fetch_all else limit
    bookmark_list = []
    offset = 0
    first = True
    while True:
        batch = client.list_bookmarks(oauth, folder_id=folder_id, limit=page_size, offset=offset)
        if not batch:
            if not first and fetch_all:
                click.echo("Warning: API returned empty mid-pagination — results may be incomplete", err=True)
            break
        bookmark_list.extend(b for b in batch if isinstance(b, dict) and b.get("type") == "bookmark")
        first = False
        if not fetch_all or len(batch) < page_size:
            break
        offset += page_size

    bodies = {}
    if deep:
        click.echo(f"Fetching article text for {len(bookmark_list)} bookmarks...", err=True)
        for b in bookmark_list:
            bid = b.get("bookmark_id")
            if bid:
                body = client.get_text(oauth, bid)
                bodies[bid] = body or ""

    results = search_bookmarks(bookmark_list, query, bodies=bodies if deep else None)

    if not results:
        click.echo("No matches found")
        return

    if json_output:
        import json
        click.echo(json.dumps(results, indent=2))
        return

    if text_index is not None:
        if text_index < 1 or text_index > len(results):
            click.echo(f"Index out of range (1-{len(results)})", err=True)
            sys.exit(1)
        bm = results[text_index - 1]
        html = bodies.get(bm["bookmark_id"]) if deep else client.get_text(oauth, bm["bookmark_id"])
        click.echo(html or "No text available")
        return

    for i, bm in enumerate(results, 1):
        progress = bm.get("progress")
        pct = f"{int(float(progress) * 100)}%" if progress is not None else "unread"
        click.echo(f"{i:>3}. {bm.get('title', 'Untitled')} ({bm.get('url', '')}) [{pct}]")
