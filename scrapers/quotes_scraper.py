from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://quotes.toscrape.com/"
START_URL = BASE_URL


def _text(node):
    return node.get_text(" ", strip=True) if node else None


def scrape_quotes(session: requests.Session, logger, timeout=20, delay=0.15):
    records, failures = [], []
    url = START_URL
    seen_pages = set()
    scraped_at = datetime.now(timezone.utc).isoformat()

    while url and url not in seen_pages:
        seen_pages.add(url)
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("div.quote")
            if not cards:
                logger.warning("No quote records found on %s", url)
                break

            for card in cards:
                try:
                    text_node = card.select_one("span.text")
                    author_node = card.select_one("small.author")
                    tags = [_text(tag) for tag in card.select("div.tags a.tag")]
                    records.append({
                        "source": "Quotes to Scrape",
                        "source_url": url,
                        "name_or_title": _text(text_node),
                        "category": None,
                        "price": None,
                        "rating": None,
                        "author": _text(author_node),
                        "tags": ", ".join(t for t in tags if t) or None,
                        "description": None,
                        "scraped_at": scraped_at,
                    })
                except Exception as exc:
                    logger.exception("Failed to parse a quote on %s: %s", url, exc)
                    failures.append({"url": url, "error": f"record_parse: {exc}"})

            next_node = soup.select_one("li.next a[href]")
            url = urljoin(url, next_node["href"]) if next_node else None
            if delay:
                import time
                time.sleep(delay)
        except requests.RequestException as exc:
            logger.error("Quote page request failed: %s - %s", url, exc)
            failures.append({"url": url, "error": f"request: {exc}"})
            break
        except Exception as exc:
            logger.exception("Unexpected quote scraper failure on %s: %s", url, exc)
            failures.append({"url": url, "error": f"unexpected: {exc}"})
            break

    logger.info("Quotes scraper collected %d records from %d pages", len(records), len(seen_pages))
    return records, failures
