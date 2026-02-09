import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, CUSTOMERS_FILE_NAME)

def transform_customer_data():
    customer_df = pd.read_parquet(RAW_PATH / CUSTOMERS_FILE_NAME)

    #clean the columns
    customer_df.columns = [c.lower() for c in customer_df.columns]

    #remove duplicate
    customer_id = customer_df.drop_duplicates(subset=['customer_id'], keep='first')

    # Fixed data type
    customer_df["signup_date"] = pd.to_datetime(customer_df["signup_date"])

    #standraze tax
    customer_df["first_name"] = customer_df["first_name"].str.title()
    customer_df["last_name"] = customer_df["last_name"].str.title()
    customer_df["gender"] = customer_df["gender"].str.title()
    customer_df["city"] = customer_df["city"].str.title()

    customer_df.to_parquet(PROCESSED_PATH / CUSTOMERS_FILE_NAME)
    return len(customer_df)
    print("transform of customer data is completed")

