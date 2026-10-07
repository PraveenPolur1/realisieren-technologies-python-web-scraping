from __future__ import annotations

import re
from urllib.parse import urlparse


def clean_text(value):
    if value is None:
        return None
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value or None


def clean_price(value):
    if value is None or str(value).strip() == "":
        return None
    match = re.search(r"[-+]?\d+(?:[.,]\d+)?", str(value).replace(",", ""))
    return float(match.group()) if match else None


def clean_rating(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        rating = int(value)
    except (TypeError, ValueError):
        return None
    return rating if 1 <= rating <= 5 else None


def clean_url(value):
    if not value:
        return None
    value = str(value).strip()
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return value
    return None


def clean_record(record):
    cleaned = dict(record)
    for field in ("source", "name_or_title", "category", "author", "tags", "description"):
        cleaned[field] = clean_text(cleaned.get(field))
    cleaned["price"] = clean_price(cleaned.get("price"))
    cleaned["rating"] = clean_rating(cleaned.get("rating"))
    cleaned["source_url"] = clean_url(cleaned.get("source_url"))
    return cleaned


def clean_records(records):
    return [clean_record(record) for record in records]
