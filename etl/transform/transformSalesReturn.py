import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, CUSTOMERS_FILE_NAME, PRODUCT_FILE_NAME
,SALES_RETURN_FILE_NAME,SALES_TRANSACTION_FILE_NAME)

# RAW_PATH = "data/raw"
# PROCESSED_PATH = "data/processed"

def transform_sales_return_data():
    print("Transforming sales return data..")

    os.makedirs(RAW_PATH, exist_ok=True)

    # Load parquet file into pandas DataFrame

    sales_returns_df= pd.read_parquet(RAW_PATH / SALES_RETURN_FILE_NAME)
    products_df = pd.read_parquet(RAW_PATH / PRODUCT_FILE_NAME)[
        ["product_id", "product_name", "category", "sub_category", "price"]
    ]
    customer_df = pd.read_parquet(RAW_PATH / CUSTOMERS_FILE_NAME)[
        ["customer_id", "first_name", "last_name", "gender", "city", "signup_date"]
    ].rename(columns={
        "first_name": "customer_first_name",
        "last_name": "customer_last_name",
        "city": "customer_city",
        "signup_date": "customer_signup_date"
    })
    sales_transaction_df = pd.read_parquet(RAW_PATH / SALES_TRANSACTION_FILE_NAME)[
        ["transaction_id", "quantity", "sale_amount", "sale_date", "last_modified"]
    ]

    # ------------ Join  -----------------------------start
    sales_returns_df = sales_returns_df.merge(sales_transaction_df, on="transaction_id", how="left")
    sales_returns_df = sales_returns_df.merge(products_df, on="product_id", how="left")
    sales_returns_df = sales_returns_df.merge(customer_df, on="customer_id", how="left")
    # ------------ Join  -----------------------------end


    # -----------------------Business Logic ___________________start
    sales_returns_df["total_amount_without_discount"] = (
        sales_returns_df["quantity"] * sales_returns_df["price"]
    )
    sales_returns_df["amount_payed_by_customer_during_return"] = (
        sales_returns_df["total_amount_without_discount"] - sales_returns_df["sale_amount"]
    )
    sales_returns_df["actual_refund_amount"] = (
        sales_returns_df["refund_amount"] - sales_returns_df["amount_payed_by_customer_during_return"]
    )
    # -----------------------Business Logic ___________________end

    # --------------Clean column names---------------start
    sales_returns_df.columns = [col.lower().replace(" ", "_") for col in sales_returns_df.columns]

    # ----------------Clean column names--------------------------------end

    # ------------- Select important columns ----------------------------start
    final_df = sales_returns_df[
        [
            "return_id",
            "transaction_id",
            "product_id",
            "customer_id",
            "customer_first_name",
            "customer_last_name",
            "customer_signup_date",
            "product_name",
            "category",
            "sub_category",
            "price",
            "return_date",
            "refund_amount",
            "reason",
            "quantity",
            "sale_amount",
            "sale_date",
            "last_modified",
            "total_amount_without_discount",
            "amount_payed_by_customer_during_return",
            "actual_refund_amount",
         ]
    ]
    # ------------- Select important columns ----------------------------end

    # ---------------Save processed data----------------start
    output_file = PROCESSED_PATH / SALES_RETURN_FILE_NAME
    final_df.to_parquet(output_file)
    return len(final_df)
    print(f"Sales Returns fact table created: {output_file}")
    print(f"Rows: {len(final_df)}")

    # ---------------Save processed data----------------end