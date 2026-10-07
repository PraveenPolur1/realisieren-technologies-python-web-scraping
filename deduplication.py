from __future__ import annotations

import re
import unicodedata


def normalize_key(value):
    if value is None:
        return ""
    value = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"\s+", " ", value).strip()


def deduplicate_records(records):
    seen = set()
    unique = []
    duplicates = []
    for record in records:
        source = normalize_key(record.get("source"))
        title = normalize_key(record.get("name_or_title"))
        author = normalize_key(record.get("author"))
        # Source + normalized title + normalized author is the business key.
        key = (source, title, author)
        if key in seen:
            duplicates.append(record)
        else:
            seen.add(key)
            unique.append(record)
    return unique, duplicates
