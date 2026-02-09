import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, PRODUCT_FILE_NAME)

"""
       Builds the Gold Product Dimension table
       Grain: 1 row per Product

       Silver responsibilities:
           - Cleaning
           - Standardization
           - Deduplication

       Gold responsibilities:
           - Business modeling
           - Surrogate keys
           - Analytics-ready schema
"""

def build_dim_product() -> None:

    print("Building Gold Dimension: Product...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    product_df = pd.read_parquet(PROCESSED_PATH / PRODUCT_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_product = product_df[[
        "product_id",
        "product_name",
        "category",
        "sub_category",
        "price",
    ]].copy()

    # Reset index to ensure clean row order before surrogate key creation
    dim_product = dim_product.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))

    # Metadata columns for lineage
    dim_product["record_source"] = "silver_product"
    dim_product["created_at"] = pd.Timestamp.now()

    dim_product.to_parquet(ANALYTICS_PATH / "dim_product.parquet", index=False)
    return len(dim_product)
    print(f"Gold Dimension Product created at {ANALYTICS_PATH} ")


