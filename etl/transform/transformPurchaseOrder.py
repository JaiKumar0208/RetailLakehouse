import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, PRODUCT_FILE_NAME
,STORE_FILE_NAME, SUPPLIES_FILE_NAME,PURCHASE_ORDER_FILE_NAME)

# RAW_PATH = "data/raw"
# PROCESSED_PATH = "data/processed"

def transform_purchase_data():
    print("Transforming Purchase Order data..")
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    purchase_orders_df = pd.read_parquet(RAW_PATH/ PURCHASE_ORDER_FILE_NAME)
    products_df = pd.read_parquet(RAW_PATH / PRODUCT_FILE_NAME)[
        ["product_id", "product_name", "category", "sub_category", "price"]
    ]
    supplier_df = pd.read_parquet(RAW_PATH / SUPPLIES_FILE_NAME)[
        ["supplier_id", "supplier_name", "city"]
    ].rename(columns={"city": "supplier_city"})
    stores_df = pd.read_parquet(RAW_PATH / STORE_FILE_NAME)[
        ["store_id", "store_name", "city", "state", "open_date"]
    ].rename(columns={"city": "store_city", "state": "store_state"})

    # ---------- Join --------------- start
    purchase_orders_df = purchase_orders_df.merge(products_df, on="product_id", how="left")
    purchase_orders_df = purchase_orders_df.merge(supplier_df, on="supplier_id", how="left")
    purchase_orders_df = purchase_orders_df.merge(stores_df, on="store_id", how="left")
    # ---------- Join --------------- end


    # Business Calculation
    purchase_orders_df["total_price"] = (
            purchase_orders_df["quantity"] * purchase_orders_df["price"]
    )

    # --------------Clean column names---------------start
    purchase_orders_df.columns= [col.lower().replace(" ", "_") for col in purchase_orders_df.columns]
    # --------------Clean column names---------------end

    # ------------- Select important columns ----------------------------start
    final_df = purchase_orders_df[
        [   "po_id",
            "supplier_id",
            "store_id",
            "product_id",
            "supplier_name",
            "supplier_city",
            "store_name",
            "store_state",
            "store_city",
            "product_name",
            "category",
            "sub_category",
            "price",
            "quantity",
            "total_price",
            "order_date",
            "delivery_date"
        ]
    ]
    # ------------- Select important columns ----------------------------end

    # ---------------Save processed data----------------start
    output_file = PROCESSED_PATH / PURCHASE_ORDER_FILE_NAME
    final_df.to_parquet(output_file)
    return len(final_df)
    print(f"purchase orders fact table created: {output_file}")
    print(f"Rows: {len(purchase_orders_df)}")
    # ---------------Save processed data----------------end