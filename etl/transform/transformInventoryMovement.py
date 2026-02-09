import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, PRODUCT_FILE_NAME
,STORE_FILE_NAME,INVENTORY_MOVEMENT_FILE_NAME)

# RAW_PATH = "data/raw"
# PROCESSED_PATH = "data/processed"

def transform_inventory_movement_data():
    print("Transforming inventory movement data..")

    os.makedirs(RAW_PATH, exist_ok=True)

    # Load parquet file into pandas DataFrame

    inventory_movement_df= pd.read_parquet(RAW_PATH / INVENTORY_MOVEMENT_FILE_NAME)
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

    # ------------ Join  -----------------------------start
    inventory_movement_df = inventory_movement_df.merge(products_df, on="product_id", how="left")
    inventory_movement_df = inventory_movement_df.merge(store_df, on="store_id", how="left")
    # ------------ Join  -----------------------------end

    # --------------Clean column names---------------start
    inventory_movement_df.columns = [col.lower().replace(" ", "_") for col in inventory_movement_df.columns]

    # ----------------Clean column names--------------------------------end


    # ------------- Select important columns ----------------------------start
    final_df = inventory_movement_df[
        [
            "movement_id",
            "store_id",
            "product_id",
            "store_name",
            "store_city",
            "store_state",
            "store_open_date",
            "product_name",
            "category",
            "sub_category",
            "price",
            "quantity_change",
            "movement_type",
            "movement_date",
         ]
    ]
    # ------------- Select important columns ----------------------------end

    # ---------------Save processed data----------------start
    output_file = PROCESSED_PATH / INVENTORY_MOVEMENT_FILE_NAME
    final_df.to_parquet(output_file)
    return len(final_df)
    print(f"Inventory Movement fact table created: {output_file}")
    print(f"Rows: {len(final_df)}")

    # ---------------Save processed data----------------end