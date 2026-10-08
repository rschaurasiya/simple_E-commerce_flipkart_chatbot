import pandas as pd
import sqlite3
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

# Folder containing csv_to_sqlite.py
BASE_DIR = Path(__file__).resolve().parent

# CSV is in the SAME folder as this Python file
csv_path = BASE_DIR / "flipkart_product_data.csv"

# SQLite database
db_path = BASE_DIR / "db_1.sqlite"


print("CSV path:")
print(csv_path)


# ============================================================
# CHECK CSV
# ============================================================

if not csv_path.exists():
    raise FileNotFoundError(
        f"\nCSV file not found:\n{csv_path}"
    )


# ============================================================
# READ CSV
# ============================================================

print("\nReading CSV...")

df = pd.read_csv(csv_path)

print(
    f"Products found in CSV: {len(df)}"
)


# ============================================================
# CLEAN DATA
# ============================================================

df = df.dropna(
    subset=["product_link"]
)

df = df.drop_duplicates(
    subset=["product_link"]
)

print(
    f"Products after cleaning: {len(df)}"
)


# ============================================================
# CONNECT TO SQLITE
# ============================================================

print("\nConnecting to SQLite...")

conn = sqlite3.connect(db_path)

cursor = conn.cursor()


# ============================================================
# CREATE PRODUCT TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_link TEXT,
    title TEXT,
    brand TEXT,
    price INTEGER,
    discount REAL,
    avg_rating REAL,
    total_ratings INTEGER
)
""")

conn.commit()


# ============================================================
# INSERT DATA
# ============================================================

print("Inserting products into SQLite...")

df.to_sql(
    "product",
    conn,
    if_exists="append",
    index=False
)

conn.commit()


# ============================================================
# VERIFY DATABASE
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM product"
)

total_products = cursor.fetchone()[0]


print("\n" + "=" * 60)
print("DATA IMPORT SUCCESSFUL")
print("=" * 60)

print(
    f"Products read from CSV : {len(df)}"
)

print(
    f"Products in SQLite     : {total_products}"
)

print(
    f"SQLite database        : {db_path}"
)

print("=" * 60)


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("\nDatabase connection closed.")