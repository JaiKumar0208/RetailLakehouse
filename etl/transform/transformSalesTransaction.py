import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, CUSTOMERS_FILE_NAME, PRODUCT_FILE_NAME
,STORE_FILE_NAME,SALES_TRANSACTION_FILE_NAME)

# RAW_PATH = "data/raw"
# PROCESSED_PATH = "data/processed"

def transform_sales_data():
    print("Transforming sales data..")
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # Load parquet into pandas DataFrame
    sales_df = pd.read_parquet(RAW_PATH / SALES_TRANSACTION_FILE_NAME)
    products_df = pd.read_parquet(RAW_PATH / PRODUCT_FILE_NAME)[
        ["product_id", "product_name", "category", "sub_category", "price"]
    ]
    store_df = pd.read_parquet(RAW_PATH / STORE_FILE_NAME)[
        ["store_id", "store_name", "city", "state", "open_date"]
    ].rename(columns={
    "city": "store_city",
    "state": "store_state",
    "open_date": "store_open_date"
})
    customer_df = pd.read_parquet(RAW_PATH / CUSTOMERS_FILE_NAME)[
        ["customer_id", "first_name", "last_name", "gender", "city", "signup_date"]
    ].rename(columns={
    "first_name" : "customer_first_name",
    "last_name" : "customer_last_name",
    "city": "customer_city",
    "signup_date": "customer_signup_date"
})



    #Example Join

    sales_df= sales_df.merge(products_df, on="product_id", how="left")
    sales_df = sales_df.merge(store_df, on="store_id", how="left")
    sales_df = sales_df.merge(customer_df, on="customer_id", how="left")

    # ------------Business Calculation-----------------start
    # Example Drive Column
    sales_df["total_amount"] = sales_df["quantity"] * sales_df["sale_amount"]
    sales_df["total_amount_without_discount"] = (
            sales_df["quantity"] * sales_df["price"]
    )
    # -------------Business Calculation----------------end


    # --------------Clean column names---------------start
    sales_df.columns = [col.lower().replace(" ", "_") for col in sales_df.columns]

    # ----------------Clean column names--------------------------------end


    # ------------- Select important columns ----------------------------start
    final_df = sales_df[
        [
            "transaction_id",
            "store_id",
            "product_id",
            "customer_id",
            "sale_date",
            "store_name",
            "store_city",
            "store_state",
            "store_open_date",
            "product_name",
            "category",
            "sub_category",
            "price",
            "customer_first_name",
            "customer_last_name",
            "customer_city",
            "gender",
            "customer_signup_date",
            "quantity",
            "sale_amount",
            "last_modified",
            "total_amount",
            "total_amount_without_discount",
        ]
    ]

    # ------------- Select important columns ----------------------------end

    # ---------------Save processed data----------------start
    output_file = PROCESSED_PATH / SALES_TRANSACTION_FILE_NAME
    final_df.to_parquet(output_file)
    return len(final_df)
    print(f"Sales fact table created: {output_file}")
    print(f"Rows: {len(final_df)}")

    # ---------------Save processed data----------------end