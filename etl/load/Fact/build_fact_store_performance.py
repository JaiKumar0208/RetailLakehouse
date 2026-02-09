import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME)

def build_fact_store_performance():
    print("Building Fact: Store Performance...")

    sales = pd.read_parquet(PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME)

    sales.rename(columns={"sale_date": "sales_date"}, inplace=True)

    fact = sales.groupby(["sales_date", "store_id"]).agg(
        total_revenue=("total_amount", "sum"),
        total_transactions=("transaction_id", "nunique"),
        total_items_sold=("quantity", "sum")
    ).reset_index()

    fact["avg_basket_size"] = fact["total_items_sold"] / fact["total_transactions"]

    fact.to_parquet(ANALYTICS_PATH / "fact_store_performance.parquet", index=False)
    return len(fact)
    print("fact_store_performance created")