import pandas as pd
import os
from config.settings import (RAW_PATH, PROCESSED_PATH, CALENDER_FILE_NAME)


def transform_calendar_data():
    print("📅 Transforming calendar data (Silver Layer)...")

    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # Load raw calendar file
    df = pd.read_parquet(RAW_PATH / CALENDER_FILE_NAME)

    # ---------------- CLEAN COLUMN NAMES ----------------
    df.columns = [c.lower().strip() for c in df.columns]

    # ---------------- STANDARDIZE DATE COLUMN ----------------
    df["date"] = pd.to_datetime(df["date"])

    # ---------------- DERIVED DATE FIELDS ----------------
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["week_of_year"] = df["date"].dt.isocalendar().week

    # Weekend flag
    df["is_weekend"] = df["day_name"].isin(["Saturday", "Sunday"])

    # ---------------- REMOVE DUPLICATES ----------------
    df = df.drop_duplicates(subset="date")

    # ---------------- SORT ----------------
    df = df.sort_values("date")

    # ---------------- SAVE SILVER FILE ----------------
    output_file = PROCESSED_PATH / CALENDER_FILE_NAME
    df.to_parquet(output_file, index=False)
    return len(df)
    print(f"Calendar Silver table created: {output_file}")
    print(f"Rows: {len(df)}")
