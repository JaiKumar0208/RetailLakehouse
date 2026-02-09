import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SUPPLIES_FILE_NAME)

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

def build_dim_supplier() -> None:

    print("Building Gold Dimension: Category...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    supplier_df = pd.read_parquet(PROCESSED_PATH / SUPPLIES_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_supplier = supplier_df[[
        "supplier_id",
        "supplier_name",
        "city",
    ]].copy()

    # Reset index to ensure clean row order before surrogate key creation
    dim_supplier = dim_supplier.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_supplier.insert(0, "supplier_key", range(1, len(dim_supplier) + 1))

    # Metadata columns for lineage
    dim_supplier["record_source"] = "silver_category"
    dim_supplier["created_at"] = pd.Timestamp.now()

    dim_supplier.to_parquet(ANALYTICS_PATH / "dim_supplier.parquet", index=False)
    return len(dim_supplier)
    print(f"Gold Dimension Supplier created at {ANALYTICS_PATH}")


