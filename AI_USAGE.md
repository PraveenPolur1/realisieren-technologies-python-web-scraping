# AI_USAGE.md

## AI Tool Used

Tool: ChatGPT (OpenAI)

## How AI Was Used

ChatGPT was used as an implementation and review assistant for this assignment. The assignment instructions explicitly allow AI coding assistants.

The assistance covered:

- interpreting the assignment requirements
- designing the standardized data model
- planning the project structure
- drafting the Requests + BeautifulSoup scraping approach
- implementing pagination using each site's public `Next` link
- drafting cleaning and validation functions
- designing normalized duplicate detection
- adding retry, timeout, and logging behavior
- creating unit tests
- drafting README documentation
- reviewing the solution against the assignment checklist

## Representative Prompts

1. "Create the complete assignment from the provided Realisieren Technologies Python Web Scraping requirements."
2. "Build a Python scraper for Books to Scrape and Quotes to Scrape with pagination, cleaning, validation, deduplication, logging, and CSV/JSON outputs."
3. "Review the implementation for missing requirements and add tests and documentation."

## AI-Assisted Parts

AI assistance was used for the initial implementation of:

- `main.py`
- `scrapers/books_scraper.py`
- `scrapers/quotes_scraper.py`
- `processing/cleaning.py`
- `processing/validation.py`
- `processing/deduplication.py`
- `tests/test_processing.py`
- `README.md`

## Human Review / Verification

The implementation was reviewed against the assignment requirements. The scraper was run against the provided public practice websites, output files were generated, and automated tests were executed.

Important review points included:

- pagination must stop naturally when there is no next page
- missing HTML elements must not crash the full process
- prices and ratings must be normalized
- duplicate matching must normalize whitespace and capitalization
- source and source URL must be preserved
- validation failures must be measurable
- logs must make failures understandable

## Incorrect or Incomplete Suggestions

No known AI-generated suggestion was intentionally retained without review. Any implementation detail was kept only after checking it against the assignment requirements and executing the project.

## Verification

Verification was performed by:

1. Installing the dependencies in an isolated environment.
2. Running `python main.py` against the two public sources.
3. Checking `output/final_dataset.csv`.
4. Checking `output/summary_report.json`.
5. Checking `logs/scraper.log`.
6. Running `pytest -q`.

## Responsibility

The final candidate is responsible for understanding the submitted implementation and being able to explain the design decisions, pagination, validation, deduplication, error handling, testing, and AI-assisted portions during the interview.
