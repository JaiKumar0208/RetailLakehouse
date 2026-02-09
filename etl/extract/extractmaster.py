import os
import pandas as pd
from sqlalchemy.orm import Session
from config.settings import OUTPUT_PATH, CUSTOMERS_FILE_NAME, PRODUCT_FILE_NAME,STORE_FILE_NAME, SUPPLIES_FILE_NAME, CATEGORIES_FILE_NAME,EMPLOYEES_FILE_NAME,CALENDER_FILE_NAME

from ServiceLayer.database import engine
from models.master.Calendar import Calendar
from models.master.Category import Category
from models.master.Customer import Customer
from models.master.Employee import Employee
from models.master.Product import Product
from models.master.Store import Store
from models.master.Supplier import Supplier

# RAW_FOLDER = "data/raw"

RAW_FOLDER = OUTPUT_PATH

def extract_table(db: Session, model, filename):
    """Generic extractor for any table"""
    print(f"🔄 Extracting {model.__tablename__}...")

    df = pd.read_sql(db.query(model).statement, db.bind)

    output_path = os.path.join(RAW_FOLDER, filename)
    df.to_parquet(output_path, index=False)

    return len(df)

    print(f"Saved {filename} ({len(df)} rows)")


def extract_master_data(db: Session):
    print("Starting MASTER data extraction...")

    os.makedirs(RAW_FOLDER, exist_ok=True)

    extract_table(db, Customer, CUSTOMERS_FILE_NAME)
    extract_table(db, Product, PRODUCT_FILE_NAME)
    extract_table(db, Store, STORE_FILE_NAME)
    extract_table(db, Supplier, SUPPLIES_FILE_NAME)
    extract_table(db, Category, CATEGORIES_FILE_NAME)
    extract_table(db, Employee, EMPLOYEES_FILE_NAME)
    extract_table(db, Calendar, CALENDER_FILE_NAME)

    print("Master data extraction completed!")

