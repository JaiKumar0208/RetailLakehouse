import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, CALENDER_FILE_NAME)

"""
       Builds the Gold Calendar Dimension table
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

def build_dim_calendar() -> None:

    print("Building Gold Dimension: Store...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    calendar_df = pd.read_parquet(PROCESSED_PATH / CALENDER_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_calendar = calendar_df.copy()

    # Reset index to ensure clean row order before surrogate key creation
    dim_calendar = dim_calendar.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_calendar.insert(0, "calendar_key", range(1, len(dim_calendar) + 1))

    # Metadata columns for lineage
    dim_calendar["record_source"] = "silver_store"
    dim_calendar["created_at"] = pd.Timestamp.now()

    dim_calendar.to_parquet(ANALYTICS_PATH / "dim_calendar.parquet", index=False)
    return len(dim_calendar)
    print(f"Gold Dimension Store created at {ANALYTICS_PATH}")


