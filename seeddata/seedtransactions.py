from ServiceLayer.transactionsDetails.InventoryMovementService import InventoryMovementService
from ServiceLayer.transactionsDetails.PaymentService import PaymentService
from ServiceLayer.transactionsDetails.PurchaseOrderService import PurchaseOrderService
from ServiceLayer.transactionsDetails.SalesReturnService import SalesReturnService
from ServiceLayer.transactionsDetails.SalesTransactionService import SalesTransactionService
from ServiceLayer.database import SessionLocal
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta


def inv_seeds(session : Session):
    print("Inventory seeds")
    for i in range(50):
        sale = InventoryMovementService.create(db=session,
            store_id=random.randint(1, 2),
            product_id=random.randint(1, 2),
            quantity_change=random.randint(1, 5),
            movement_type=random.uniform(100, 1000),
            movement_date=datetime.now()
        )

def seed_sales_transactions(db: Session, num_records: int = 100):
    print("Seeding sales transactions...")

    for _ in range(num_records):
        quantity = random.randint(1, 5)
        price_per_unit = random.uniform(100, 1000)
        sale_amount = round(quantity * price_per_unit, 2)

        sale_date = datetime.now() - timedelta(days=random.randint(1, 60))

        SalesTransactionService.create(
            db=db,
            store_id=random.randint(1, 2),  # Must exist in stores
            product_id=random.randint(1, 2),  # Must exist in products
            customer_id=random.randint(1, 2),  # Must exist in customers
            quantity=quantity,
            sale_amount=sale_amount,
            sale_date=sale_date,
            last_modified=datetime.now()
            )

        print("✅ Sales transactions seeded successfully!")


PAYMENT_METHODS = ["CASH", "CARD", "UPI", "NETBANKING"]

def seed_payments(db: Session, num_records: int = 50):
    print("Seeding payment data...")

    for i in range(50):
        PaymentService.create(
            db=db,
            transaction_id=random.randint(1, 99),
            payment_method=random.choice(PAYMENT_METHODS),
            payment_date=datetime.now() - timedelta(days=random.randint(0, 30)),
            amount=round(random.uniform(100, 2000), 2)
        )

    print("✅ Payments seeded successfully!")


def seed_purchase_orders(db: Session, num_records: int = 30):
    print("Seeding purchase orders...")

    for _ in range(num_records):
        order_date = datetime.now() - timedelta(days=random.randint(10, 60))

        # 70% chance the order is delivered
        if random.random() < 0.7:
            delivery_date = order_date + timedelta(days=random.randint(1, 10))
        else:
            delivery_date = None

        PurchaseOrderService.create(
            db=db,
            supplier_id=random.randint(1, 2),  # Must exist in suppliers table
            store_id=random.randint(1, 2),  # Must exist in stores table
            product_id=random.randint(1, 2),  # Must exist in products table
            quantity=random.randint(10, 200),
            order_date=order_date,
            delivery_date=delivery_date
            )

        print("✅ Purchase orders seeded successfully!")

def seed_sales_returns(db: Session, num_records: int = 20):
    print("Seeding sales returns...")

    reasons = [
        "Damaged item",
        "Wrong product delivered",
        "Customer changed mind",
        "Defective product",
        "Late delivery"
        ]

    for _ in range(num_records):
        # Return happens after a sale (1–30 days later)
        return_date = datetime.now() - timedelta(days=random.randint(1, 30))

        SalesReturnService.create(
            db=db,
            transaction_id=random.randint(1, 99),  # Must exist in sales_transactions
            product_id=random.randint(1, 2),  # Must exist in products
            customer_id=random.randint(1, 2),  # Must exist in customers
            return_date=return_date,
            refund_amount=round(random.uniform(50, 500), 2),
            reason=random.choice(reasons)
            )

        print("✅ Sales returns seeded successfully!")



def main():
    db = SessionLocal()
    try:
        inv_seeds(db)
        seed_sales_transactions(db, num_records=100)
        seed_payments(db, num_records=50)
        seed_purchase_orders(db, num_records=30)
        seed_sales_returns(db, num_records=20)

        db.commit()
        print("✅ Transaction data seeded successfully!")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding transactions:", e)
    finally:
        db.close()

if __name__ == "__main__":
     main()