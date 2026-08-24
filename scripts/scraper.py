import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

URL = "https://books.toscrape.com/"

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "raw" / "books.csv"


# Download website
response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# Get all books
books = soup.select("article.product_pod h3 a")


# Create CSV if it doesn't exist
if not CSV_FILE.exists():

    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["row_number", "book_name"]
        )

        writer.writeheader()


# Count existing books
with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)
    existing_books = list(reader)


books_scraped = len(existing_books)


# Stop if all 20 books are already collected
if books_scraped >= len(books):

    print("All books on this page have been scraped.")

else:

    # Select next book
    book = books[books_scraped]

    book_data = {
        "row_number": books_scraped + 1,
        "book_name": book["title"]
    }


    # Save dictionary to CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["row_number", "book_name"]
        )

        writer.writerow(book_data)


    print(book_data)