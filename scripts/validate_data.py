import pandas as pd
from pathlib import Path


# -----------------------------
# File paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "books_clean.csv"


# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv(INPUT_FILE)


print("=" * 50)
print("DATA VALIDATION REPORT")
print("=" * 50)


# -----------------------------
# 1. Check row count
# -----------------------------

row_count = len(df)

print(f"\nRows: {row_count}")

if row_count > 0:
    print("PASS: Dataset contains rows")
else:
    print("FAIL: Dataset is empty")


# -----------------------------
# 2. Check required columns
# -----------------------------

required_columns = [
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

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if not missing_columns:
    print("PASS: All required columns exist")
else:
    print(f"FAIL: Missing columns: {missing_columns}")


# -----------------------------
# 3. Check duplicate UPCs
# -----------------------------

duplicate_upcs = df["upc"].duplicated().sum()

print(f"\nDuplicate UPCs: {duplicate_upcs}")

if duplicate_upcs == 0:
    print("PASS: No duplicate UPCs")
else:
    print("FAIL: Duplicate UPCs found")


# -----------------------------
# 4. Check missing important values
# -----------------------------

important_columns = [
    "book_name",
    "upc",
    "price_excl_tax",
    "price_incl_tax",
]

print("\nMissing values:")

validation_failed = False

for column in important_columns:

    missing = df[column].isna().sum()

    print(f"{column}: {missing}")

    if missing > 0:
        validation_failed = True

if not validation_failed:
    print("PASS: No missing values in important columns")
else:
    print("FAIL: Missing values found")


# -----------------------------
# 5. Check numeric columns
# -----------------------------

numeric_columns = [
    "price_excl_tax",
    "price_incl_tax",
    "tax",
    "stock_count",
    "rating",
]

print("\nNumeric column validation:")

for column in numeric_columns:

    if pd.api.types.is_numeric_dtype(df[column]):
        print(f"PASS: {column} is numeric")
    else:
        print(f"FAIL: {column} is NOT numeric")
        validation_failed = True


# -----------------------------
# 6. Check negative prices
# -----------------------------

negative_prices = (
    (df["price_excl_tax"] < 0).sum()
    + (df["price_incl_tax"] < 0).sum()
)

print(f"\nNegative price values: {negative_prices}")

if negative_prices == 0:
    print("PASS: No negative prices")
else:
    print("FAIL: Negative prices found")


# -----------------------------
# 7. Check negative stock
# -----------------------------

negative_stock = (df["stock_count"] < 0).sum()

print(f"Negative stock values: {negative_stock}")

if negative_stock == 0:
    print("PASS: No negative stock values")
else:
    print("FAIL: Negative stock values found")


# -----------------------------
# 8. Check rating range
# -----------------------------

invalid_ratings = (
    ~df["rating"].between(1, 5)
).sum()

print(f"\nInvalid ratings: {invalid_ratings}")

if invalid_ratings == 0:
    print("PASS: Ratings are between 1 and 5")
else:
    print("FAIL: Invalid ratings found")


# -----------------------------
# Final result
# -----------------------------

print("\n" + "=" * 50)

if (
    row_count > 0
    and not missing_columns
    and duplicate_upcs == 0
    and not validation_failed
    and negative_prices == 0
    and negative_stock == 0
    and invalid_ratings == 0
):

    print("FINAL RESULT: DATASET PASSED VALIDATION")

else:

    print("FINAL RESULT: DATASET FAILED VALIDATION")

print("=" * 50)

