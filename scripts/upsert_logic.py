from pathlib import Path
import pandas as pd
import duckdb
from clean_data import Data
import os

# === CONFIG ===
BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")
DUCKDB_FILE = "food_prices.duckdb"
TABLE_NAME = "food_price_history"
clean_data = Data()

# Ensure silver directory exists
SILVER_DIR.mkdir(parents=True, exist_ok=True)

# === UTILS ===
import os
import pandas as pd
import duckdb

DUCKDB_FILE = "your_duckdb_file.duckdb"  # Replace with your actual DuckDB file path
TABLE_NAME = "food_price_history"        # Replace with your actual table name


def get_merge_key_columns(df: pd.DataFrame) -> list:
    if all(col in df.columns for col in ["date", "state", "region"]):
        return ["date", "state", "region"]
    elif all(col in df.columns for col in ["date", "region"]):
        return ["date", "region"]
    else:
        raise ValueError("❌ Unknown key combination — can't determine unique ID.")


def run_upsert(parquet_file: str, df: pd.DataFrame):
    key_cols = get_merge_key_columns(df)
    con = duckdb.connect(DUCKDB_FILE)

    # Check if the table already exists
    existing_tables = con.execute("SHOW TABLES").fetchdf()["name"].tolist()
    table_exists = TABLE_NAME in existing_tables

    if not table_exists:
        # Create table with schema from Parquet file (but no data)
        con.execute(f"""
            CREATE TABLE {TABLE_NAME} AS
            SELECT * FROM read_parquet('{parquet_file}') WHERE FALSE
        """)
        # Add primary key constraint on first creation
        con.execute(f"""
            ALTER TABLE {TABLE_NAME}
            ADD CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ({', '.join(key_cols)})
        """)
        print(f"🆕 Created table and added primary key on: {key_cols}")

    # Get current DuckDB table schema
    existing_cols_df = con.execute(f"PRAGMA table_info('{TABLE_NAME}')").fetchdf()
    existing_cols = set(existing_cols_df["name"].str.lower())
    new_cols = set(col.lower() for col in df.columns)

    # Add new columns to DuckDB
    for col in new_cols - existing_cols:
        con.execute(f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{col}" VARCHAR')
        print(f"➕ Added column to DuckDB: '{col}'")

    # Add missing columns to DataFrame
    for col in existing_cols - new_cols:
        df = df.copy()
        df[col] = None
        print(f"⚠️ Added missing column to DataFrame: '{col}'")

    # Re-save to align schema
    df.to_parquet(parquet_file, index=False)

    # Create temp view from aligned Parquet file
    con.execute(f"""
        CREATE OR REPLACE TEMP VIEW new_data AS
        SELECT * FROM read_parquet('{parquet_file}')
    """)

    # Quote column names for SQL
    quoted_cols = [f'"{col}"' for col in df.columns]
    columns = ", ".join(quoted_cols)
    select_expr = ", ".join([f"source.{col}" for col in quoted_cols])
    update_expr = ", ".join([
        f"{col} = EXCLUDED.{col}" for col in quoted_cols
        if col.strip('"').lower() not in [k.lower() for k in key_cols]
    ])

    # Run UPSERT (DuckDB-style)
    sql = f"""
        INSERT INTO {TABLE_NAME} ({columns})
        SELECT {select_expr} FROM new_data AS source
        ON CONFLICT ({', '.join([f'"{k}"' for k in key_cols])})
        DO UPDATE SET {update_expr}
    """

    con.execute(sql)
    print(f"✅ Upserted {os.path.basename(parquet_file)} using keys: {key_cols}")


# def get_merge_key_columns(df: pd.DataFrame) -> list:
#     if all(col in df.columns for col in ["date", "state", "region"]):
#         return ["date", "state", "region"]
#     elif all(col in df.columns for col in ["date", "region"]):
#         return ["date", "region"]
#     else:
#         raise ValueError("❌ Unknown key combination — can't determine unique ID.")
    
# def run_upsert(parquet_file: str, df: pd.DataFrame):
#     key_cols = get_merge_key_columns(df)
#     con = duckdb.connect(DUCKDB_FILE)

#     # Create table if it doesn't exist
#     con.execute(f"""
#         CREATE TABLE IF NOT EXISTS {TABLE_NAME} AS
#         SELECT * FROM read_parquet('{parquet_file}') WHERE FALSE
#     """)

#     # Get existing DuckDB table columns
#     existing_cols_df = con.execute(f"PRAGMA table_info('{TABLE_NAME}')").fetchdf()
#     existing_cols = set(existing_cols_df["name"].str.lower())
#     new_cols = set(col.lower() for col in df.columns)

#     # Add new columns to DuckDB
#     for col in new_cols - existing_cols:
#         con.execute(f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{col}" VARCHAR')
#         print(f"➕ Added column to DuckDB: '{col}'")

#     # Add missing columns to DataFrame
#     for col in existing_cols - new_cols:
#         df = df.copy()
#         df[col] = None
#         print(f"⚠️ Added missing column to DataFrame: '{col}'")

#     # Re-save to align schema
#     df.to_parquet(parquet_file, index=False)

#     # Create temp view
#     con.execute(f"""
#         CREATE OR REPLACE TEMP VIEW new_data AS
#         SELECT * FROM read_parquet('{parquet_file}')
#     """)

#     # Try to add PRIMARY KEY constraint (only works once)
#     try:
#         con.execute(f"""
#             ALTER TABLE {TABLE_NAME}
#             ADD CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY ({', '.join(key_cols)})
#         """)
#     except Exception as e:
#         if "Duplicate" not in str(e):
#             print(f"⚠️ Could not add primary key constraint: {e}")

#     # Build insert/update SQL
#     columns = ", ".join(df.columns)
#     select_expr = ", ".join([f"source.{col}" for col in df.columns])
#     update_expr = ", ".join([f"{col} = EXCLUDED.{col}" for col in df.columns if col not in key_cols])

#     sql = f"""
#         INSERT INTO {TABLE_NAME} ({columns})
#         SELECT {select_expr} FROM new_data AS source
#         ON CONFLICT ({', '.join(key_cols)})
#         DO UPDATE SET {update_expr}
#     """

#     con.execute(sql)
#     print(f"✅ Upserted {os.path.basename(parquet_file)} using keys: {key_cols}")

# def run_upsert(parquet_file: str, df: pd.DataFrame):
#     key_cols = get_merge_key_columns(df)
#     con = duckdb.connect(DUCKDB_FILE)

#     # Create table if it doesn't exist
#     con.execute(f"""
#         CREATE TABLE IF NOT EXISTS {TABLE_NAME} AS
#         SELECT * FROM read_parquet('{parquet_file}') WHERE FALSE
#     """)

#     # Get current DuckDB table schema
#     existing_cols_df = con.execute(f"PRAGMA table_info('{TABLE_NAME}')").fetchdf()
#     existing_cols = set(existing_cols_df["name"].str.lower())
#     new_cols = set(col.lower() for col in df.columns)

#     # Add new columns to DuckDB
#     for col in new_cols - existing_cols:
#         con.execute(f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{col}" VARCHAR')
#         print(f"➕ Added column to DuckDB: '{col}'")

#     # Add missing columns to DataFrame (if table has more than DataFrame)
#     for col in existing_cols - new_cols:
#         df = df.copy()
#         df[col] = None
#         print(f"⚠️ Added missing column to DataFrame: '{col}'")

#     # Re-save to align schema
#     df.to_parquet(parquet_file, index=False)

#     # Create temp view
#     con.execute(f"""
#         CREATE OR REPLACE TEMP VIEW new_data AS
#         SELECT * FROM read_parquet('{parquet_file}')
#     """)

#     key_condition = " AND ".join([f"target.{col} = source.{col}" for col in key_cols])

#     # Perform MERGE
#     con.execute(f"""
#         MERGE INTO {TABLE_NAME} AS target
#         USING new_data AS source
#         ON {key_condition}
#         WHEN MATCHED THEN UPDATE SET *
#         WHEN NOT MATCHED THEN INSERT *
#     """)

#     print(f"✅ Upserted {os.path.basename(parquet_file)} using keys: {key_cols}")

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
