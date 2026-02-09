from typing import Optional, List
from sqlalchemy.orm import Session
from models.transactionsDetails.SalesTransaction import SalesTransaction
from datetime import datetime

class SalesTransactionService:

    @staticmethod
    def create(
        db: Session,
        store_id: int,
        product_id: int,
        customer_id: int,
        quantity: int,
        sale_amount,
        sale_date,
        last_modified=None
    ) -> SalesTransaction:
        """Create a new sales transaction"""
        transaction = SalesTransaction(
            store_id=store_id,
            product_id=product_id,
            customer_id=customer_id,
            quantity=quantity,
            sale_amount=sale_amount,
            sale_date=sale_date,
            last_modified=last_modified
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_id(db: Session, transaction_id: int) -> Optional[SalesTransaction]:
        """Get sales transaction by ID"""
        return db.query(SalesTransaction).filter(
            SalesTransaction.transaction_id == transaction_id
        ).first()

    @staticmethod
    def get_all(db: Session) -> List[SalesTransaction]:
        """Get all sales transactions"""
        return db.query(SalesTransaction).all()

    @staticmethod
    def get_by_store(db: Session, store_id: int) -> List[SalesTransaction]:
        """Get all transactions for a store"""
        return db.query(SalesTransaction).filter(
            SalesTransaction.store_id == store_id
        ).all()

    @staticmethod
    def get_by_customer(db: Session, customer_id: int) -> List[SalesTransaction]:
        """Get all transactions for a customer"""
        return db.query(SalesTransaction).filter(
            SalesTransaction.customer_id == customer_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        transaction_id: int,
        quantity: int = None,
        sale_amount=None,
        last_modified=None
    ) -> Optional[SalesTransaction]:
        """Update a sales transaction"""
        transaction = db.query(SalesTransaction).filter(
            SalesTransaction.transaction_id == transaction_id
        ).first()

        if not transaction:
            return None

        if quantity is not None:
            transaction.quantity = quantity
        if sale_amount is not None:
            transaction.sale_amount = sale_amount
        if last_modified is not None:
            transaction.last_modified = last_modified

        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete(db: Session, transaction_id: int) -> bool:
        """Delete a sales transaction"""
        transaction = db.query(SalesTransaction).filter(
            SalesTransaction.transaction_id == transaction_id
        ).first()

        if not transaction:
            return False

        db.delete(transaction)
        db.commit()
        return True

    @staticmethod
    def soft_delete_payment(db: Session, transaction_id: int):
        transaction = db.query(SalesTransaction).filter(SalesTransaction.transaction_id == transaction_id).first()
        if transaction:
            transaction.deleted_at = datetime.now()
            db.commit()
