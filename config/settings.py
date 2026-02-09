from pathlib import Path

# SET FILE DIRECTORY
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_PATH = BASE_DIR/"data/raw"
PROCESSED_PATH = BASE_DIR/"data/processed"
OUTPUT_PATH = BASE_DIR / "data/raw"
ANALYTICS_PATH = BASE_DIR / "data/analytics"

# SET FILE NAME SLIVER LAYER
#--------MSTER DATA------------
CALENDER_FILE_NAME = "calendar.parquet"
CATEGORIES_FILE_NAME = "categories.parquet"
CUSTOMERS_FILE_NAME = "customers.parquet"
EMPLOYEES_FILE_NAME = "employees.parquet"
PRODUCT_FILE_NAME = "product.parquet"
STORE_FILE_NAME = "store.parquet"
SUPPLIES_FILE_NAME = "suppliers.parquet"

#---------------TRANSACTION DATA------------
INVENTORY_MOVEMENT_FILE_NAME = "inventory_movements.parquet"
PAYMENTS_FILE_NAME = "payments.parquet"
PURCHASE_ORDER_FILE_NAME = "purchase_orders.parquet"
SALES_RETURN_FILE_NAME = "sales_returns.parquet"
SALES_TRANSACTION_FILE_NAME= "sales_transaction.parquet"
