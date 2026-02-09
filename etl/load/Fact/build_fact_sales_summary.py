import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME)

SILVER_PATH = PROCESSED_PATH
GOLD_PATH = ANALYTICS_PATH

def build_gold_sales_summary():
    print("Creating Gold Sales Summary...")

    os.makedirs(GOLD_PATH, exist_ok=True)

    sales_df = pd.read_parquet(SILVER_PATH / SALES_TRANSACTION_FILE_NAME)

    sales_df.rename(columns={"sale_date": "sales_date"}, inplace=True)

    gold_df = sales_df.groupby(
        ["sales_date", "store_id"]
    ).agg(
        total_sales_amount=("total_amount", "sum"),
        total_quantity_sold=("quantity", "sum"),
        total_transactions=("transaction_id", "nunique")
    ).reset_index()

    gold_df["avg_transaction_value"] = (
        gold_df["total_sales_amount"] / gold_df["total_transactions"]
    )

    gold_df.to_parquet(f"{GOLD_PATH}/gold_sales_summary.parquet", index=False)
    return len(gold_df)
    print("Gold Sales Summary Created")
