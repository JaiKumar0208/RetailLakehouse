import os
import pandas as pd
from sqlalchemy.orm import Session
from ServiceLayer.database import engine
from models.transactionsDetails.PurchaseOrder import PurchaseOrder
from config.settings import OUTPUT_PATH,PURCHASE_ORDER_FILE_NAME

PURCHASE_ORDERS_FILE = OUTPUT_PATH / PURCHASE_ORDER_FILE_NAME

# OUTPUT_PATH = "data/raw/purchase_orders.parquet"


def extract_purchase_orders_to_parquet(db: Session):
    print("Starting purchase order extraction...")

    # Create DB session
    # Query all purchase order
    query = db.query(PurchaseOrder)

    # Convert to Pandas DataFrame
    df = pd.read_sql(query.statement, db.bind)

    # Ensure raw folder exists
    os.makedirs(os.path.dirname(PURCHASE_ORDERS_FILE), exist_ok=True)

    # Save to Parquet
    df.to_parquet(PURCHASE_ORDERS_FILE, index=False)
    return len(df)
    print(f"Extraction complete. File saved to {PURCHASE_ORDERS_FILE}")
    print(f"Rows extracted: {len(df)}")


