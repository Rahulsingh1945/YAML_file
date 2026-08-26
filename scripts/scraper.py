import csv
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"

CSV_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "books.csv"
)

FIELDNAMES = [
    "book_name",
    "category",
    "price_excl_tax",
    "price_incl_tax",
    "tax",
    "availability",
    "stock_count",
    "rating",
    "upc",
    "product_url",
    "image_url",
    "description",
    "page_number",
    "scraped_at",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_soup(url):
    """Download a page and return BeautifulSoup object."""

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_table_value(soup, field_name):
    """Extract a value from the product information table."""

    rows = soup.select(
        "table.table-striped tr"
    )

    for row in rows:

        header = row.find("th")
        value = row.find("td")

        if header and value:

            if header.get_text(
                strip=True
            ) == field_name:

                return value.get_text(
                    strip=True
                )

    return None


def get_rating(soup):
    """Convert star rating into an integer."""

    rating_element = soup.select_one(
        "div.product_main p.star-rating"
    )

    if not rating_element:
        return None

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    for class_name in rating_element.get(
        "class",
        []
    ):

        if class_name in ratings:
            return ratings[class_name]

    return None


def get_stock_count(availability):
    """Extract stock quantity from availability text."""

    if not availability:
        return None

    match = re.search(
        r"\d+",
        availability
    )

    if match:
        return int(match.group())

    return None


def scrape_book(
    product_url,
    page_number
):
    """Scrape detailed information from one book."""

    soup = get_soup(product_url)

    # -----------------------------
    # Book name
    # -----------------------------

    title_element = soup.select_one(
        "div.product_main h1"
    )

    book_name = None

    if title_element:
        book_name = title_element.get_text(
            strip=True
        )

    # -----------------------------
    # Category
    # -----------------------------

    category_links = soup.select(
        "ul.breadcrumb li a"
    )

    category = None

    if len(category_links) >= 3:

        category = category_links[2].get_text(
            strip=True
        )

    # -----------------------------
    # Price
    # -----------------------------

    price_excl_tax = get_table_value(
        soup,
        "Price (excl. tax)"
    )

    price_incl_tax = get_table_value(
        soup,
        "Price (incl. tax)"
    )

    tax = get_table_value(
        soup,
        "Tax"
    )

    # -----------------------------
    # Availability
    # -----------------------------

    availability = get_table_value(
        soup,
        "Availability"
    )

    stock_count = get_stock_count(
        availability
    )

    # -----------------------------
    # UPC
    # -----------------------------

    upc = get_table_value(
        soup,
        "UPC"
    )

    # -----------------------------
    # Image
    # -----------------------------

    image_element = soup.select_one(
        "div.item.active img"
    )

    image_url = None

    if image_element:

        image_url = urljoin(
            product_url,
            image_element.get("src")
        )

    # -----------------------------
    # Description
    # -----------------------------

    description = None

    description_element = soup.select_one(
        "#product_description + p"
    )

    if description_element:

        description = description_element.get_text(
            " ",
            strip=True
        )

    # -----------------------------
    # Final record
    # -----------------------------

    return {
        "book_name": book_name,
        "category": category,
        "price_excl_tax": price_excl_tax,
        "price_incl_tax": price_incl_tax,
        "tax": tax,
        "availability": availability,
        "stock_count": stock_count,
        "rating": get_rating(soup),
        "upc": upc,
        "product_url": product_url,
        "image_url": image_url,
        "description": description,
        "page_number": page_number,
        "scraped_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


def save_book(book_data):
    """Save a book only if its UPC is not already in the CSV."""

    CSV_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    existing_upcs = set()

    if CSV_FILE.exists():

        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                if row.get("upc"):
                    existing_upcs.add(row["upc"])

    if book_data.get("upc") in existing_upcs:
        print(f"Already exists: {book_data['book_name']}")
        return

    file_exists = CSV_FILE.exists()

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(book_data)

        print(f"Added: {book_data['book_name']}")


def scrape_page(page_number):
    """Scrape one catalogue page and all books on it."""

    if page_number == 1:

        page_url = BASE_URL

    else:

        page_url = urljoin(
            BASE_URL,
            f"catalogue/page-{page_number}.html"
        )

    print()
    print("=" * 60)
    print(
        f"SCRAPING PAGE "
        f"{page_number}/50"
    )
    print("=" * 60)

    soup = get_soup(page_url)

    books = soup.select(
        "article.product_pod h3 a"
    )

    print(
        f"Books found: {len(books)}"
    )

    for index, book in enumerate(
        books,
        start=1
    ):

        relative_url = book.get(
            "href"
        )

        product_url = urljoin(
            page_url,
            relative_url
        )

        print(
            f"[Page {page_number} - "
            f"Book {index}/{len(books)}]"
        )

        try:

            book_data = scrape_book(
                product_url,
                page_number
            )

            save_book(book_data)

            print(
                f"✓ {book_data['book_name']}"
            )

        except Exception as error:

            print(
                f"✗ Failed: {product_url}"
            )

            print(
                f"  Error: {error}"
            )

        time.sleep(0.2)


def main():

    print("=" * 60)
    print("BOOK SCRAPER STARTED")
    print("=" * 60)

    for page_number in range(1, 51):

        scrape_page(page_number)

    print()
    print("=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    print(
        f"Data saved to: {CSV_FILE}"
    )


if __name__ == "__main__":
    main()