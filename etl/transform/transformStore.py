import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, STORE_FILE_NAME)

def transform_store_data():

    store_df = pd.read_parquet(RAW_PATH / STORE_FILE_NAME)

    # Clean column names
    store_df.columns = [c.lower() for c in store_df.columns]

    # remove duplicate
    store_df = store_df.drop_duplicates(subset="store_id")

    # Fix data types
    store_df["open_date"] = pd.to_datetime(store_df["open_date"])

    # Standardize text
    store_df["store_name"] = store_df["store_name"].str.title()
    store_df["city"] = store_df["city"].str.title()
    store_df["state"] = store_df["state"].str.title()

    store_df.to_parquet(PROCESSED_PATH / STORE_FILE_NAME, index=False)
    return len(store_df)
    print("transform of product data is completed")