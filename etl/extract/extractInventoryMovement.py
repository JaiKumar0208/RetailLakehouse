import os
import pandas as pd
from sqlalchemy.orm import Session
from ServiceLayer.database import engine
from models.transactionsDetails.InventoryMovement import InventoryMovement
from config.settings import OUTPUT_PATH,INVENTORY_MOVEMENT_FILE_NAME

# OUTPUT_PATH = "data/raw/inventory_movements.parquet"

INVENTORY_MOVEMENT_FILE= OUTPUT_PATH / INVENTORY_MOVEMENT_FILE_NAME

def extract_inventory_movements_to_parquet(db: Session):
    print("Starting inventory movements extraction...")

    # Create DB session

    # Query all inventory movements
    query = db.query(InventoryMovement)

    # Convert to Pandas DataFrame
    df = pd.read_sql(query.statement, db.bind)

    # Ensure raw folder exists
    os.makedirs(os.path.dirname(INVENTORY_MOVEMENT_FILE), exist_ok=True)

    # Save to Parquet
    df.to_parquet(INVENTORY_MOVEMENT_FILE, index=False)

    return len(df)

    print(f"Extraction complete. File saved to {INVENTORY_MOVEMENT_FILE}")
    print(f"Rows extracted: {len(df)}")

# if __name__ == "__main__":
#     extract_inventory_movements_to_parquet()
