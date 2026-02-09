import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, EMPLOYEES_FILE_NAME)

"""
       Builds the Gold Employee Dimension table
       Grain: 1 row per Employee

       Silver responsibilities:
           - Cleaning
           - Standardization
           - Deduplication

       Gold responsibilities:
           - Business modeling
           - Surrogate keys
           - Analytics-ready schema
"""

def build_dim_employee() -> None:

    print("Building Gold Dimension: Employee...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    employee_df = pd.read_parquet(PROCESSED_PATH / EMPLOYEES_FILE_NAME)

    # Customer Dimension
    # Select business-relevant attributes
    dim_employee = employee_df[[
        "employee_id",
        "employee_name",
        "store_id",
        "salary",
        "dob"
    ]].copy()

    # Rename for business-friendly warehouse naming
    dim_employee.rename(columns={
        "dob": "employee_date_of_birth",
    }, inplace=True)

    # Reset index to ensure clean row order before surrogate key creation
    dim_employee = dim_employee.reset_index(drop=True)

    # Add surrogate key (warehouse primary key)
    dim_employee.insert(0, "employee_key", range(1, len(dim_employee) + 1))

    # Metadata columns for lineage
    dim_employee["record_source"] = "silver_employee"
    dim_employee["created_at"] = pd.Timestamp.now()

    dim_employee.to_parquet(ANALYTICS_PATH / "dim_employee.parquet", index=False)
    return len(dim_employee)
    print(f"Gold Dimension Employee created at {ANALYTICS_PATH} ")


