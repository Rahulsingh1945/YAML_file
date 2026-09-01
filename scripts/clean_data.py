import pandas as pd
from pathlib import Path


# -----------------------------
# File paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "books.csv"
CLEAN_FILE = BASE_DIR / "data" / "processed" / "books_clean.csv"


# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv(RAW_FILE)

original_rows = len(df)

print("Original rows:", original_rows)
print("Original columns:", len(df.columns))
print()


# -----------------------------
# 1. Remove completely empty rows
# -----------------------------

df = df.dropna(how="all")


# -----------------------------
# 2. Remove duplicate books
# -----------------------------

if "upc" in df.columns:
    df = df.drop_duplicates(subset="upc", keep="first")
else:
    df = df.drop_duplicates(subset="book_name", keep="first")


# -----------------------------
# 3. Clean text columns
# -----------------------------

text_columns = [
    "book_name",
    "category",
    "availability",
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# -----------------------------
# 4. Convert numeric columns
# -----------------------------

# -----------------------------
# 4. Clean numeric columns
# -----------------------------

numeric_columns = [
    "price_excl_tax",
    "price_incl_tax",
    "tax",
    "stock_count",
]

for column in numeric_columns:
    if column in df.columns:

        # Remove currency symbols and other non-numeric characters
        df[column] = (
            df[column]
            .astype("string")
            .str.replace("£", "", regex=False)
            .str.replace("Â", "", regex=False)
            .str.strip()
        )

        # Convert to numeric
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# -----------------------------
# 5. Validate price values
# -----------------------------

price_columns = [
    "price_excl_tax",
    "price_incl_tax",
    "tax",
]

for column in price_columns:
    if column in df.columns:
        df.loc[
            df[column] < 0,
            column
        ] = pd.NA


# Stock cannot be negative
if "stock_count" in df.columns:
    df.loc[
        df["stock_count"] < 0,
        "stock_count"
    ] = pd.NA
# -----------------------------
# 6. Validate stock count
# -----------------------------

if "stock_count" in df.columns:
    df.loc[
        df["stock_count"] < 0,
        "stock_count"
    ] = pd.NA


# -----------------------------
# 7. Remove rows without UPC
# -----------------------------

if "upc" in df.columns:
    df = df.dropna(subset=["upc"])


# -----------------------------
# 8. Reset index
# -----------------------------

df = df.reset_index(drop=True)


# -----------------------------
# 9. Create processed folder
# -----------------------------

CLEAN_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# 10. Save cleaned dataset
# -----------------------------

df.to_csv(
    CLEAN_FILE,
    index=False
)


# -----------------------------
# Cleaning summary
# -----------------------------

clean_rows = len(df)

print("Clean rows:", clean_rows)
print("Rows removed:", original_rows - clean_rows)
print("Final columns:", len(df.columns))
print()
print("Cleaned file saved to:")
print(CLEAN_FILE)