import os
import pandas as pd
from config.settings import (RAW_PATH, PROCESSED_PATH, OUTPUT_PATH, EMPLOYEES_FILE_NAME)


def transform_employee_data():

    employee_df = pd.read_parquet(RAW_PATH / EMPLOYEES_FILE_NAME)

    #clean columns
    employee_df.columns = [c.lower() for c in employee_df.columns]

    # remove duplicate
    employee_df = employee_df.drop_duplicates(subset=['employee_id'], keep='first')

    # fixed data type
    employee_df["dob"] = pd.to_datetime(employee_df["dob"])

    #standarzation text

    employee_df["employee_name"] = employee_df["employee_name"].str.title()

    employee_df.to_parquet(PROCESSED_PATH / EMPLOYEES_FILE_NAME)
    return len(employee_df)
    print("Transforming employee data...")