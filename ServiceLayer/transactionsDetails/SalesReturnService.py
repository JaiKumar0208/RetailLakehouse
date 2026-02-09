from typing import Optional, List
from sqlalchemy.orm import Session
from models.transactionsDetails.SalesReturn import SalesReturn
from datetime import datetime

class SalesReturnService:

    @staticmethod
    def create(
        db: Session,
        transaction_id: int,
        product_id: int,
        customer_id: int,
        return_date,
        refund_amount,
        reason: str = None
    ) -> SalesReturn:
        """Create a new sales return record"""
        sales_return = SalesReturn(
            transaction_id=transaction_id,
            product_id=product_id,
            customer_id=customer_id,
            return_date=return_date,
            refund_amount=refund_amount,
            reason=reason
        )
        db.add(sales_return)
        db.commit()
        db.refresh(sales_return)
        return sales_return

    @staticmethod
    def get_by_id(db: Session, return_id: int) -> Optional[SalesReturn]:
        """Get a return record by ID"""
        return db.query(SalesReturn).filter(
            SalesReturn.return_id == return_id
        ).first()

    @staticmethod
    def get_all(db: Session) -> List[SalesReturn]:
        """Get all return records"""
        return db.query(SalesReturn).all()

    @staticmethod
    def get_by_customer(db: Session, customer_id: int) -> List[SalesReturn]:
        """Get all returns for a specific customer"""
        return db.query(SalesReturn).filter(
            SalesReturn.customer_id == customer_id
        ).all()

    @staticmethod
    def get_by_transaction(db: Session, transaction_id: int) -> List[SalesReturn]:
        """Get returns linked to a specific sales transaction"""
        return db.query(SalesReturn).filter(
            SalesReturn.transaction_id == transaction_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        return_id: int,
        refund_amount=None,
        reason: str = None
    ) -> Optional[SalesReturn]:
        """Update return details"""
        sales_return = db.query(SalesReturn).filter(
            SalesReturn.return_id == return_id
        ).first()

        if not sales_return:
            return None

        if refund_amount is not None:
            sales_return.refund_amount = refund_amount
        if reason is not None:
            sales_return.reason = reason

        db.commit()
        db.refresh(sales_return)
        return sales_return

    @staticmethod
    def delete(db: Session, return_id: int) -> bool:
        """Delete a return record"""
        sales_return = db.query(SalesReturn).filter(
            SalesReturn.return_id == return_id
        ).first()

        if not sales_return:
            return False

        db.delete(sales_return)
        db.commit()
        return True

    @staticmethod
    def soft_delete_payment(db: Session, return_id: int):
        sales_return = db.query(SalesReturn).filter(SalesReturn.return_id == return_id).first()
        if sales_return:
            sales_return.deleted_at = datetime.now()
            db.commit()
