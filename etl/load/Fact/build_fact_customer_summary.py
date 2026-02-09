import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME)

def build_fact_customer_summary():
    print("Building Fact: Customer Summary...")

    sales = pd.read_parquet(PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME)

    sales.rename(columns={"sale_date": "sales_date"}, inplace=True)

    fact = sales.groupby("customer_id").agg(
        total_orders=("transaction_id", "nunique"),
        total_spent=("total_amount", "sum"),
        avg_order_value=("total_amount", "mean"),
        first_purchase_date=("sales_date", "min"),
        last_purchase_date=("sales_date", "max")
    ).reset_index()

    fact.to_parquet(ANALYTICS_PATH / "fact_customer_summary.parquet", index=False)
    return len(fact)
    print("fact_customer_summary created")
