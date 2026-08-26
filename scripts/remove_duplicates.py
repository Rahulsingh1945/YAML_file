import pandas as pd
from pathlib import Path


CSV_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "books.csv"


df = pd.read_csv(CSV_FILE)

before = len(df)

print("Before cleaning:", before)

df = df.drop_duplicates(
    subset="upc",
    keep="first"
)

after = len(df)

df.to_csv(
    CSV_FILE,
    index=False,
    encoding="utf-8"
)

print("After cleaning:", after)
print("Removed:", before - after)