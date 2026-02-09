import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, CUSTOMERS_FILE_NAME)

"""
       Builds the Gold Customer Dimension table
       Grain: 1 row per customer

       Silver responsibilities:
           - Cleaning
           - Standardization
           - Deduplication

       Gold responsibilities:
           - Business modeling
           - Surrogate keys
           - Analytics-ready schema
"""

def build_dim_customers() -> None:

    print("Building Gold Dimension: Customers...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    customers_df = pd.read_parquet(PROCESSED_PATH / CUSTOMERS_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_customers = customers_df[[
        "customer_id",
        "first_name",
        "last_name",
        "gender",
        "city",
        "signup_date"
    ]].copy()

    # Rename for business-friendly warehouse naming
    dim_customers.rename(columns={
        "first_name": "customer_first_name",
        "last_name": "customer_flast_name",
        "gender": "customer_gender",
        "city": "customer_city",
        "signup_date": "customer_signup_date",
    }, inplace=True)

    # Reset index to ensure clean row order before surrogate key creation
    dim_customers = dim_customers.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_customers.insert(0, "customer_key", range(1, len(dim_customers) + 1))

    # Metadata columns for lineage
    dim_customers["record_source"] = "silver_customers"
    dim_customers["created_at"] = pd.Timestamp.now()

    dim_customers.to_parquet(ANALYTICS_PATH / "dim_customers.parquet", index=False)
    return len(dim_customers)
    print(f"Gold Dimension Customers created at {ANALYTICS_PATH} ")


