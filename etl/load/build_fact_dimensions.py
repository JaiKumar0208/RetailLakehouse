import os
import pandas as pd
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, CUSTOMERS_FILE_NAME
, PRODUCT_FILE_NAME, STORE_FILE_NAME, CALENDER_FILE_NAME,SALES_TRANSACTION_FILE_NAME)

def build_gold_sales_model():
    print("🚀 Building Gold Layer with surrogate keys...")

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    # ---------------- LOAD SILVER DATA ---------------- #
    customers_df = pd.read_parquet(PROCESSED_PATH / CUSTOMERS_FILE_NAME)
    products_df = pd.read_parquet(PROCESSED_PATH / PRODUCT_FILE_NAME)
    stores_df = pd.read_parquet(PROCESSED_PATH / STORE_FILE_NAME)
    calendar_df = pd.read_parquet(PROCESSED_PATH / CALENDER_FILE_NAME)
    sales_df = pd.read_parquet(PROCESSED_PATH / "fact_sales_transactions.parquet")

    # ---------------- DIMENSIONS ---------------- #
    print("🧱 Creating dimension tables with surrogate keys...")

    # Customer Dimension
    dim_customers = customers_df.drop_duplicates(subset="customer_id").copy()
    dim_customers = dim_customers.reset_index(drop=True)
    dim_customers["customer_sk"] = dim_customers.index + 1

    # Product Dimension
    dim_products = products_df.drop_duplicates(subset="product_id").copy()
    dim_products = dim_products.reset_index(drop=True)
    dim_products["product_sk"] = dim_products.index + 1

    # Store Dimension
    dim_stores = stores_df.drop_duplicates(subset="store_id").copy()
    dim_stores = dim_stores.reset_index(drop=True)
    dim_stores["store_sk"] = dim_stores.index + 1

    # Date Dimension
    dim_date = calendar_df.drop_duplicates(subset="date").copy()
    dim_date = dim_date.reset_index(drop=True)
    dim_date["date_sk"] = dim_date.index + 1
    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)

    # ---------------- FACT TABLE ---------------- #
    print("📊 Creating fact table with surrogate keys...")

    sales_df = sales_df.copy()
    sales_df["date_key"] = pd.to_datetime(sales_df["sale_date"]).dt.strftime("%Y%m%d").astype(int)

    # Map natural keys to surrogate keys
    fact_sales = sales_df.merge(dim_customers[["customer_id", "customer_sk"]], on="customer_id", how="left")
    fact_sales = fact_sales.merge(dim_products[["product_id", "product_sk"]], on="product_id", how="left")
    fact_sales = fact_sales.merge(dim_stores[["store_id", "store_sk"]], on="store_id", how="left")
    fact_sales = fact_sales.merge(dim_date[["date_key", "date_sk"]], on="date_key", how="left")

    # Keep only surrogate keys + measures
    fact_sales_final = fact_sales[
        [
            "transaction_id",
            "date_sk",
            "customer_sk",
            "product_sk",
            "store_sk",
            "quantity",
            "sale_amount",
            "total_amount",
            "total_amount_without_discount",
        ]
    ]

    # ---------------- SAVE GOLD FILES ---------------- #
    print("💾 Saving Gold Layer tables with SKs...")

    dim_customers.to_parquet(ANALYTICS_PATH / "dim_customers.parquet", index=False)
    dim_products.to_parquet(ANALYTICS_PATH / "dim_products.parquet", index=False)
    dim_stores.to_parquet(ANALYTICS_PATH / "dim_stores.parquet", index=False)
    dim_date.to_parquet(ANALYTICS_PATH / "dim_date.parquet", index=False)
    fact_sales_final.to_parquet(ANALYTICS_PATH / "fact_sales.parquet", index=False)

    print("✅ Gold Layer with surrogate keys built!")
    print(f"📂 Output location: {ANALYTICS_PATH}")
    print(f"📊 Fact rows: {len(fact_sales_final)}")
