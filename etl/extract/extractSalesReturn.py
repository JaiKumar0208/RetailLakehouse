import os
import pandas as pd
from sqlalchemy.orm import Session
from ServiceLayer.database import engine
from models.transactionsDetails.SalesReturn import SalesReturn
from config.settings import OUTPUT_PATH, SALES_RETURN_FILE_NAME

# OUTPUT_PATH = "data/raw/sales_returns.parquet"
SALES_RETURN_FILE = OUTPUT_PATH / SALES_RETURN_FILE_NAME

def extract_sales_return_to_parquet(db: Session):
    print("Starting sales return extraction...")

    # Create DB session
    # Query all sales return
    query = db.query(SalesReturn)

    # Convert to Pandas DataFrame
    df = pd.read_sql(query.statement, db.bind)

    # Ensure raw folder exists
    os.makedirs(os.path.dirname(SALES_RETURN_FILE), exist_ok=True)

    # Save to Parquet
    df.to_parquet(SALES_RETURN_FILE, index=False)
    return len(df)
    print(f"Extraction complete. File saved to {SALES_RETURN_FILE}")
    print(f"Rows extracted: {len(df)}")

