from __future__ import annotations

REQUIRED_FIELDS = ("source", "source_url", "name_or_title")


def validate_record(record):
    errors = []
    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append(f"missing_{field}")

    if record.get("price") is not None and not isinstance(record["price"], (int, float)):
        errors.append("price_not_numeric")
    if record.get("rating") is not None:
        if not isinstance(record["rating"], int) or not 1 <= record["rating"] <= 5:
            errors.append("rating_out_of_range")
    if record.get("source") not in {"Books to Scrape", "Quotes to Scrape"}:
        errors.append("unknown_source")
    url = record.get("source_url") or ""
    if not (url.startswith("http://") or url.startswith("https://")):
        errors.append("invalid_source_url")
    return len(errors) == 0, errors


def validate_records(records):
    valid, rejected = [], []
    for record in records:
        ok, errors = validate_record(record)
        if ok:
            valid.append(record)
        else:
            rejected.append({"record": record, "errors": errors})
    return valid, rejected
