import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, CATEGORIES_FILE_NAME)

def transform_category_data():

    category_df = pd.read_parquet(RAW_PATH / CATEGORIES_FILE_NAME)

    # Clean column names
    category_df.columns = [c.lower() for c in category_df.columns]

    # remove duplicate
    customer_df = category_df.drop_duplicates(subset="category_id")

    # Fix data types

    # Standardize text
    category_df["category_name"] = category_df["category_name"].str.title()
    category_df["description"] = category_df["description"].str.title()

    category_df.to_parquet(PROCESSED_PATH / CATEGORIES_FILE_NAME, index=False)
    return len(category_df)
    print("transform of category data is completed")