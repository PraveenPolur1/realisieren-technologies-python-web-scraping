from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_records
from processing.validation import validate_records
from processing.deduplication import deduplicate_records

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

COLUMNS = [
    "source", "source_url", "name_or_title", "category", "price",
    "rating", "author", "tags", "description", "scraped_at"
]


def configure_logging():
    logger = logging.getLogger("realisieren_scraper")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def build_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Realisieren-Assignment-Scraper/1.0 (educational)"})
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def main():
    start = time.perf_counter()
    logger = configure_logging()
    logger.info("Starting consolidated scraping pipeline")
    session = build_session()

    source_results = {}
    all_records = []
    all_failures = []

    for source_name, scraper in [
        ("Books to Scrape", scrape_books),
        ("Quotes to Scrape", scrape_quotes),
    ]:
        try:
            records, failures = scraper(session, logger)
        except Exception as exc:
            logger.exception("Source %s failed unexpectedly: %s", source_name, exc)
            records, failures = [], [{"source": source_name, "error": f"fatal: {exc}"}]
        source_results[source_name] = {"collected": len(records), "failures": len(failures)}
        all_records.extend(records)
        all_failures.extend(failures)

    cleaned = clean_records(all_records)
    valid, rejected = validate_records(cleaned)
    unique, duplicates = deduplicate_records(valid)

    dataframe = pd.DataFrame(unique, columns=COLUMNS)
    dataframe.to_csv(OUTPUT_DIR / "final_dataset.csv", index=False)

    elapsed = round(time.perf_counter() - start, 3)
    summary = {
        "sources": source_results,
        "total_records_collected": len(all_records),
        "total_records_after_cleaning": len(cleaned),
        "records_rejected_during_validation": len(rejected),
        "duplicate_records_detected_or_removed": len(duplicates),
        "final_record_count": len(unique),
        "scraping_failures": len(all_failures),
        "execution_time_seconds": elapsed,
        "validation_rejections": rejected[:100],
        "scraping_failures_detail": all_failures[:100],
    }
    with open(OUTPUT_DIR / "summary_report.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    logger.info("Completed: %d final records, %d rejected, %d duplicates, %.3fs", len(unique), len(rejected), len(duplicates), elapsed)
    print(json.dumps({k: summary[k] for k in (
        "total_records_collected", "records_rejected_during_validation",
        "duplicate_records_detected_or_removed", "final_record_count", "execution_time_seconds"
    )}, indent=2))


if __name__ == "__main__":
    main()
