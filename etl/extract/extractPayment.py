import os
import pandas as pd
from sqlalchemy.orm import Session
from ServiceLayer.database import engine
from models.transactionsDetails.Payment import Payment
from config.settings import OUTPUT_PATH,PAYMENTS_FILE_NAME

# OUTPUT_PATH = "data/raw/payments.parquet"
PAYMENTS_FILE = OUTPUT_PATH / PAYMENTS_FILE_NAME

def extract_payment_to_parquet(db: Session):
    print("Starting payment extraction...")

    # Create DB session
    # Query all payment
    query = db.query(Payment)

    # Convert to Pandas DataFrame
    df = pd.read_sql(query.statement, db.bind)

    # Ensure raw folder exists
    os.makedirs(os.path.dirname(PAYMENTS_FILE), exist_ok=True)

    # Save to Parquet
    df.to_parquet(PAYMENTS_FILE, index=False)
    return len(df)
    print(f"Extraction complete. File saved to {PAYMENTS_FILE}")
    print(f"Rows extracted: {len(df)}")

