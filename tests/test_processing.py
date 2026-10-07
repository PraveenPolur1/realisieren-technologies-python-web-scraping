from processing.cleaning import clean_price, clean_rating, clean_text
from processing.validation import validate_record
from processing.deduplication import deduplicate_records


def test_clean_text():
    assert clean_text("  Hello   world \n") == "Hello world"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating(5) == 5
    assert clean_rating(6) is None


def test_validation():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/item.html",
        "name_or_title": "Example",
        "price": 10.0,
        "rating": 4,
    }
    assert validate_record(record)[0] is True


def test_deduplication_normalizes_title():
    records = [
        {"source": "Books to Scrape", "name_or_title": "Example Book ", "author": None},
        {"source": "Books to Scrape", "name_or_title": "EXAMPLE BOOK", "author": None},
    ]
    unique, duplicates = deduplicate_records(records)
    assert len(unique) == 1
    assert len(duplicates) == 1
