from etl.extract.extractInventoryMovement import extract_inventory_movements_to_parquet
from etl.extract.extractmaster import extract_master_data
from etl.extract.extractPayment import extract_payment_to_parquet
from etl.extract.extractPurchaseOrder import extract_purchase_orders_to_parquet
from etl.extract.extractSalesReturn import extract_sales_return_to_parquet
from etl.extract.extractSalesTransaction import extract_sales_transaction_to_parquet
from ServiceLayer.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        extract_inventory_movements_to_parquet(db)
        extract_master_data(db)
        extract_payment_to_parquet(db)
        extract_purchase_orders_to_parquet(db)
        extract_sales_return_to_parquet(db)
        extract_sales_transaction_to_parquet(db)
        db.commit()
        print("✅ parquet file generated successfully!")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding create parquet file:", e)
    finally:
        db.close()


if __name__ == "__main__":
    main()