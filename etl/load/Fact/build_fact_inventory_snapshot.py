import pandas as pd
import os
from config.settings import (PROCESSED_PATH, ANALYTICS_PATH, INVENTORY_MOVEMENT_FILE_NAME)

def build_fact_inventory_snapshot():
    print("Building Fact: Inventory Snapshot...")

    inventory = pd.read_parquet(PROCESSED_PATH / INVENTORY_MOVEMENT_FILE_NAME)

    fact = inventory.groupby(["store_id", "product_id"]).agg(
        stock_on_hand=("quantity_change", "last"),
        last_updated=("movement_date", "max")
    ).reset_index()

    fact.to_parquet(ANALYTICS_PATH / "fact_inventory_snapshot.parquet", index=False)
    return len(fact)
    print("fact_inventory_snapshot created")



