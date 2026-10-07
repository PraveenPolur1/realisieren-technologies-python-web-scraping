# Realisieren Technologies – Multi-Source Web Scraping Assignment

## 1. Overview

This project implements a reusable Python pipeline that scrapes two public practice websites:

- Books to Scrape: https://books.toscrape.com/
- Quotes to Scrape: https://quotes.toscrape.com/

The pipeline performs scraping, pagination, cleaning, validation, duplicate detection, consolidation, logging, and output generation.

## 2. Python Version

Python 3.10+ recommended. The solution uses standard Python features plus Requests, BeautifulSoup, Pandas, and Pytest.

## 3. Project Structure

```text
realisieren_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
├── logs/
│   └── scraper.log
├── tests/
│   └── test_processing.py
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## 4. Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Run

From the project root:

```bash
python main.py
```

The scraper follows each site's pagination links rather than hard-coding a fixed page count. The Books scraper starts at the first catalogue page and follows the `Next` link. The Quotes scraper starts at the home page and follows its `Next` link until no next page exists.

## 6. Standard Data Model

The consolidated dataset uses:

- `source`
- `source_url`
- `name_or_title`
- `category`
- `price`
- `rating`
- `author`
- `tags`
- `description`
- `scraped_at`

Fields that do not apply to a source remain null rather than being invented.

## 7. Scraping Approach

### Books to Scrape

The scraper selects product cards and extracts title, price, availability-derived information where available, rating, and product URL. Source-specific selectors are isolated in `scrapers/books_scraper.py`.

### Quotes to Scrape

The scraper selects quote cards and extracts quote text, author, tags, and page URL. Source-specific selectors are isolated in `scrapers/quotes_scraper.py`.

## 8. Cleaning

Cleaning is kept separate from scraping in `processing/cleaning.py`:

- collapse repeated whitespace
- trim text
- convert price strings such as `£51.77` to numeric values
- normalize ratings to integers from 1–5
- validate-looking HTTP/HTTPS URLs
- represent empty values as `None`

## 9. Validation

Before consolidation, records are checked for:

- source
- source URL
- title/name
- numeric price when present
- rating between 1 and 5 when present
- recognized source name

Rejected records and their validation reasons are recorded in the summary report.

## 10. Deduplication

Duplicates are identified using a normalized business key:

`source + normalized name_or_title + normalized author`

Normalization uses Unicode normalization, case folding, whitespace collapsing, and trimming. This catches equivalent values such as `Example Book`, ` Example Book `, and `EXAMPLE BOOK`. The first occurrence is retained and later equivalent records are counted as duplicates.

## 11. Error Handling and Logging

Requests use timeouts and a small retry policy for transient HTTP failures. Missing elements are handled without crashing the entire run. A failed page is logged and the affected source is stopped cleanly while the other source can still run.

Logs are written to `logs/scraper.log` and also displayed in the console.

## 12. Outputs

`output/final_dataset.csv` contains the final standardized records.

`output/summary_report.json` contains:

- records collected per source
- total records collected
- records after cleaning
- validation rejections
- duplicate count
- final record count
- scraping failures
- execution time

## 13. Tests

Run:

```bash
pytest -q
```

The tests cover text cleaning, price conversion, rating validation, record validation, and normalized duplicate detection.

## 14. Assumptions

- The provided practice websites remain publicly accessible.
- Their public HTML structure is sufficiently stable for the selectors used.
- Source-specific fields that are not present in the common model are stored as null.
- Duplicate detection is intentionally conservative and source-aware.

## 15. Known Limitations

- The scraper depends on the public HTML structure of the practice sites.
- It does not use browser automation because the sources do not require JavaScript for the required data.
- A page-level request failure is logged rather than endlessly retried.
- Book category/description are left null because this implementation does not make an additional request for every book detail page.

## 16. AI Usage

See `AI_USAGE.md` for the required AI-assistance disclosure.
