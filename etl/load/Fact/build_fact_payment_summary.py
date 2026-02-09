import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, PAYMENTS_FILE_NAME)

def build_fact_payment_summary():
    print("Building Fact: Payment Summary...")

    payments = pd.read_parquet(PROCESSED_PATH / PAYMENTS_FILE_NAME)

    fact = payments.groupby(["payment_date", "payment_method"]).agg(
        total_amount=("amount", "sum"),
        total_transactions=("transaction_id", "nunique")
    ).reset_index()

    fact.to_parquet(ANALYTICS_PATH / "fact_payment_summary.parquet", index=False)
    return len(fact)
    print("fact_payment_summary created")


