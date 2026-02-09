import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, SUPPLIES_FILE_NAME)

def transform_supplier_data():

    supplier_df = pd.read_parquet(RAW_PATH / SUPPLIES_FILE_NAME)

    # Clean column names
    supplier_df.columns = [c.lower() for c in supplier_df.columns]

    # remove duplicate
    store_df = supplier_df.drop_duplicates(subset="supplier_id")

    # Fix data types

    # Standardize text
    supplier_df["supplier_name"] = supplier_df["supplier_name"].str.title()
    supplier_df["city"] = supplier_df["city"].str.title()

    supplier_df.to_parquet(PROCESSED_PATH / SUPPLIES_FILE_NAME, index=False)
    return len(supplier_df)
    print("transform of product data is completed")