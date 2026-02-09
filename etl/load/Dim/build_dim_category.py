import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, CATEGORIES_FILE_NAME)

"""
       Builds the Gold Category Dimension table
       Grain: 1 row per Category

       Silver responsibilities:
           - Cleaning
           - Standardization
           - Deduplication

       Gold responsibilities:
           - Business modeling
           - Surrogate keys
           - Analytics-ready schema
"""

def build_dim_Category() -> None:

    print("Building Gold Dimension: Category...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    category_df = pd.read_parquet(PROCESSED_PATH / CATEGORIES_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_category = category_df[[
        "category_id",
        "category_name",
        "description",
    ]].copy()

    # Reset index to ensure clean row order before surrogate key creation
    dim_category = dim_category.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_category.insert(0, "category_key", range(1, len(dim_category) + 1))

    # Metadata columns for lineage
    dim_category["record_source"] = "silver_category"
    dim_category["created_at"] = pd.Timestamp.now()

    dim_category.to_parquet(ANALYTICS_PATH / "dim_category.parquet", index=False)
    return len(dim_category)
    print(f"Gold Dimension category created at {ANALYTICS_PATH} ")


