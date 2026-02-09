import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, SALES_TRANSACTION_FILE_NAME)

def build_fact_product_performance():
    print("Building Fact: Product Performance...")

    sales = pd.read_parquet(PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME)

    sales.rename(columns={"sale_date": "sales_date"}, inplace=True)

    fact = sales.groupby(["sales_date", "product_id"]).agg(
        total_quantity_sold=("quantity", "sum"),
        total_sales_amount=("total_amount", "sum")
    ).reset_index()

    fact["avg_selling_price"] = fact["total_sales_amount"] / fact["total_quantity_sold"]

    fact.to_parquet(ANALYTICS_PATH / "fact_product_performance.parquet", index=False)
    return len(fact)
    print("fact_product_performance created")