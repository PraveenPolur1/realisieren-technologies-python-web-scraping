from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")


def _text(node):
    return node.get_text(" ", strip=True) if node else None


def _rating(node):
    if not node:
        return None
    classes = node.get("class", [])
    words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for word, value in words.items():
        if word in classes:
            return value
    return None


def scrape_books(session: requests.Session, logger, timeout=20, delay=0.15):
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
            cards = soup.select("article.product_pod")
            if not cards:
                logger.warning("No book records found on %s", url)
                break

            for card in cards:
                try:
                    title_node = card.select_one("h3 a")
                    price_node = card.select_one(".price_color")
                    availability_node = card.select_one(".availability")
                    rating_node = card.select_one("p.star-rating")
                    product_href = title_node.get("href") if title_node else None
                    records.append({
                        "source": "Books to Scrape",
                        "source_url": urljoin(url, product_href) if product_href else None,
                        "name_or_title": title_node.get("title", _text(title_node)) if title_node else None,
                        "category": None,
                        "price": _text(price_node),
                        "rating": _rating(rating_node),
                        "author": None,
                        "tags": None,
                        "description": None,
                        "scraped_at": scraped_at,
                    })
                except Exception as exc:
                    logger.exception("Failed to parse a book on %s: %s", url, exc)
                    failures.append({"url": url, "error": f"record_parse: {exc}"})

            next_node = soup.select_one("li.next a[href]")
            url = urljoin(url, next_node["href"]) if next_node else None
            if delay:
                import time
                time.sleep(delay)
        except requests.RequestException as exc:
            logger.error("Book page request failed: %s - %s", url, exc)
            failures.append({"url": url, "error": f"request: {exc}"})
            # Stop this source cleanly; other sources can still run.
            break
        except Exception as exc:
            logger.exception("Unexpected book scraper failure on %s: %s", url, exc)
            failures.append({"url": url, "error": f"unexpected: {exc}"})
            break

    logger.info("Books scraper collected %d records from %d pages", len(records), len(seen_pages))
    return records, failures
