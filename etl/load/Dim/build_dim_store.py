import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, STORE_FILE_NAME)

"""
       Builds the Gold Store Dimension table
       Grain: 1 row per store

       Silver responsibilities:
           - Cleaning
           - Standardization
           - Deduplication

       Gold responsibilities:
           - Business modeling
           - Surrogate keys
           - Analytics-ready schema
"""

def build_dim_store() -> None:

    print("Building Gold Dimension: Store...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    store_df = pd.read_parquet(PROCESSED_PATH / STORE_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_store = store_df[[
        "store_id",
        "store_name",
        "city",
        "state",
        "open_date"
    ]].copy()

    # Rename for business-friendly warehouse naming
    dim_store.rename(columns={
        "open_date": "store_signup_date",
    }, inplace=True)

    # Reset index to ensure clean row order before surrogate key creation
    dim_store = dim_store.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_store.insert(0, "store_key", range(1, len(dim_store) + 1))

    # Metadata columns for lineage
    dim_store["record_source"] = "silver_store"
    dim_store["created_at"] = pd.Timestamp.now()

    dim_store.to_parquet(ANALYTICS_PATH / "dim_store.parquet", index=False)
    return len(dim_store)
    print(f"Gold Dimension Store created at {ANALYTICS_PATH}")


