from pathlib import Path
import pandas as pd
import duckdb
from clean_data import CleanData
import os

# === CONFIG ===
BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")
DUCKDB_FILE = "food_prices.duckdb"
TABLE_NAME = "food_price_history"
clean_data = CleanData()

# Ensure silver directory exists
SILVER_DIR.mkdir(parents=True, exist_ok=True)

def get_merge_key_columns(df: pd.DataFrame) -> list:
    if all(col in df.columns for col in ["date", "state", "region"]):
        return ["date", "state", "region"]
    elif all(col in df.columns for col in ["date", "region"]):
        return ["date", "region"]
    else:
        raise ValueError("❌ Unknown key combination — can't determine unique ID.")

def run_upsert(parquet_file: str, df: pd.DataFrame):
    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Ensure 'state' column exists for region-level data
    if 'state' not in df.columns:
        df['state'] = "ALL"

    # Ensure date column is proper DATE type
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # Determine keys
    key_cols = get_merge_key_columns(df)

    con = duckdb.connect(DUCKDB_FILE)

    # Check if table exists
    existing_tables = con.execute("SHOW TABLES").fetchdf()["name"].tolist()
    table_exists = TABLE_NAME in existing_tables

    if not table_exists:
        # Create table and primary key
        con.execute(f"""
            CREATE TABLE {TABLE_NAME} AS
            SELECT * FROM read_parquet('{parquet_file}') WHERE FALSE
        """)
        con.execute(f"""
            ALTER TABLE {TABLE_NAME}
            ADD CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ({', '.join(key_cols)})
        """)
        print(f"🆕 Created table and added primary key on: {key_cols}")

    # Ensure schema matches — add new columns if needed
    existing_cols_df = con.execute(f"PRAGMA table_info('{TABLE_NAME}')").fetchdf()
    existing_cols = set(existing_cols_df["name"].str.lower())
    new_cols = set(df.columns)

    for col in new_cols - existing_cols:
        con.execute(f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{col}" VARCHAR')
        print(f"➕ Added column to DuckDB: '{col}'")

    for col in existing_cols - new_cols:
        df[col] = None
        print(f"⚠️ Added missing column to DataFrame: '{col}'")

    # Save aligned dataframe
    df.to_parquet(parquet_file, index=False)

    # Upsert with ON CONFLICT
    quoted_cols = [f'"{col}"' for col in df.columns]
    columns = ", ".join(quoted_cols)
    select_expr = ", ".join([f"source.{col}" for col in quoted_cols])
    update_expr = ", ".join([
        f"{col} = EXCLUDED.{col}" for col in quoted_cols
        if col.strip('"').lower() not in [k.lower() for k in key_cols]
    ])

    sql = f"""
        INSERT INTO {TABLE_NAME} ({columns})
        SELECT {select_expr} FROM read_parquet('{parquet_file}') AS source
        ON CONFLICT ({', '.join([f'"{k}"' for k in key_cols])})
        DO UPDATE SET {update_expr}
    """

    con.execute(sql)
    print(f"✅ Upserted {os.path.basename(parquet_file)} using keys: {key_cols}")


# === MAIN LOOP ===

counter = 0
for file in BRONZE_DIR.glob("*.xlsx"):
    try:
        if file.name.startswith("~$"):  # Skip temporary Excel lock files
            continue

        date_ = clean_data.extract_date_from_filename(file)
        date_ = pd.to_datetime(date_, dayfirst=True)

        if pd.Timestamp("2017-01-01") <= date_ <= pd.Timestamp("2022-12-31"):
            continue
        elif date_.year == 2016:
            df = clean_data.clean_2016_data(file)
            print(df.columns)
        elif date_.year == 2023 and date_.month == 1:
            df = clean_data.clean_01_2017_01_2023(file)
            print(df.columns)
        elif date_.year == 2023 and date_.month in [2,3,4, 5, 7, 8]:
            df = clean_data.clean_02_2023_08_2023(file)
            print(df.columns)
        elif date_.year == 2023 and date_.month == 6:
            df = clean_data.clean_june_2023(file)
            print(df.columns)
        else:
            df = clean_data.clean_incremental(file)
            print(df.columns)
        
        
        # Save to Silver
        parquet_filename = SILVER_DIR / (file.stem + ".parquet")
        df.to_parquet(parquet_filename, index=False)

        # Run upsert
        run_upsert(str(parquet_filename), df)
        print("successfully upsert")
        counter += 1

    except Exception as e:
        print(f"❌ Failed to process {file.name}: {e}")

print(f"\n🎉 Finished processing and upserting {counter} files.")
