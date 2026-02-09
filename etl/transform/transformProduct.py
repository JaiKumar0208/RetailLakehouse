import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, PRODUCT_FILE_NAME)

def transform_product_data():

    product_df = pd.read_parquet(RAW_PATH / PRODUCT_FILE_NAME)

    # Clean column names
    product_df.columns = [c.lower() for c in product_df.columns]

    # remove duplicate
    product_df = product_df.drop_duplicates(subset="product_id")

    # Fix data types
    product_df["price"] =  product_df["price"].astype("float64")
    product_df["price"] = product_df["price"].round(2)

    # Standardize text
    product_df["product_name"] = product_df["product_name"].str.title()
    product_df["category"] = product_df["category"].str.title()
    product_df["sub_category"] = product_df["sub_category"].str.title()

    product_df.to_parquet(PROCESSED_PATH / PRODUCT_FILE_NAME, index=False)
    return len(product_df)
    print("transform of product data is completed")