import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME, PRODUCT_FILE_NAME)

def build_fact_category_performance():
    print("Building Fact: Sales Performance...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # Load Silver sales data
    sales = pd.read_parquet(PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME)

    sales.rename(columns={
        "sale_date": "sales_date",
    }, inplace=True)

    # Aggregate daily sales metrics
    fact = sales.groupby("sales_date").agg(
        total_orders=("transaction_id", "count"),
        total_quantity_sold=("quantity", "sum"),
        total_sales_amount=("total_amount", "sum")
    ).reset_index()

    # Add surrogate key
    fact.insert(0, "sales_performance_key", range(1, len(fact) + 1))

    # Metadata
    fact["record_source"] = "silver_sales"
    fact["created_at"] = pd.Timestamp.now()

    # Save Gold fact
    fact.to_parquet(ANALYTICS_PATH / "fact_sales_performance.parquet", index=False)
    return len(fact)
    print(" fact_sales_performance created")
