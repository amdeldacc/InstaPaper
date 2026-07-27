def search_bookmarks(bookmarks: list, query: str, bodies: dict | None = None) -> list:
    q = query.lower()
    results = []
    for b in bookmarks:
        fields = [
            b.get("title", ""),
            b.get("description", ""),
            b.get("url", ""),
        ]
        fields.extend(t.get("name", "") for t in b.get("tags", []))
        if bodies and b.get("bookmark_id") in bodies:
            fields.append(bodies[b["bookmark_id"]])
        if any(q in f.lower() for f in fields):
            results.append(b)
    return results
