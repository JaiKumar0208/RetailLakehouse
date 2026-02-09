import os
import pandas as pd
from sqlalchemy.orm import Session
from ServiceLayer.database import engine
from models.transactionsDetails.SalesTransaction import SalesTransaction
from config.settings import OUTPUT_PATH, SALES_TRANSACTION_FILE_NAME

# OUTPUT_PATH = "data/raw/sales_transactions.parquet"
SALES_TRANSACTION_FILE = OUTPUT_PATH / SALES_TRANSACTION_FILE_NAME

def extract_sales_transaction_to_parquet(db: Session):
    print("Starting sales extraction...")

    # Create DB session
    # Query all sales transactions
    query = db.query(SalesTransaction)

    # Convert to Pandas DataFrame
    df = pd.read_sql(query.statement, db.bind)

    # Ensure raw folder exists
    os.makedirs(os.path.dirname(SALES_TRANSACTION_FILE), exist_ok=True)

    # Save to Parquet
    df.to_parquet(SALES_TRANSACTION_FILE, index=False)
    return len(df)
    print(f"Extraction complete. File saved to {SALES_TRANSACTION_FILE}")
    print(f"Rows extracted: {len(df)}")

