import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME)

def build_fact_daily_kpis():
    print("Building Fact: Daily KPIs...")

    sales = pd.read_parquet(PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME)

    sales.rename(columns={"sale_date": "sales_date"}, inplace=True)

    fact = sales.groupby("sales_date").agg(
        total_revenue=("total_amount", "sum"),
        total_transactions=("transaction_id", "nunique"),
        total_customers=("customer_id", "nunique"),
        total_items_sold=("quantity", "sum")
    ).reset_index()

    fact["avg_order_value"] = fact["total_revenue"] / fact["total_transactions"]

    fact.to_parquet(ANALYTICS_PATH / "fact_daily_kpis.parquet", index=False)
    return len(fact)
    print("fact_daily_kpis created")

