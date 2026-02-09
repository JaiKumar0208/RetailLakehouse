from typing import Optional, List, Any
from sqlalchemy.orm import Session
from models import Payment
from models.transactionsDetails.Payment import Payment
from datetime import datetime

class PaymentService:

    @staticmethod
    def create(
        db: Session,
        transaction_id: int,
        payment_method: str,
        payment_date,
        amount
    ) -> Payment:
        """Create a new payment record"""
        payment = Payment(
            transaction_id=transaction_id,
            payment_method=payment_method,
            payment_date=payment_date,
            amount=amount
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_by_id(db: Session, payment_id: int) -> Optional[Payment]:
        """Get payment by ID"""
        return db.query(Payment).filter(Payment.payment_id == payment_id).first()

    @staticmethod
    def get_all(db: Session) -> list[type[Payment]]:
        """Get all payments"""
        return db.query(Payment).all()

    @staticmethod
    def get_by_transaction(db: Session, transaction_id: int) -> list[type[Payment]]:
        """Get payments for a specific sales transaction"""
        return db.query(Payment).filter(
            Payment.transaction_id == transaction_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        payment_id: int,
        payment_method: str = None,
        payment_date=None,
        amount=None
    ) -> type[Payment] | None:
        """Update payment details"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            return None

        if payment_method is not None:
            payment.payment_method = payment_method
        if payment_date is not None:
            payment.payment_date = payment_date
        if amount is not None:
            payment.amount = amount

        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def delete(db: Session, payment_id: int) -> bool:
        """Delete a payment"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            return False

        db.delete(payment)
        db.commit()
        return True

    @staticmethod
    def soft_delete_payment(db: Session, payment_id: int):
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if payment:
            payment.deleted_at = datetime.now()
            db.commit()
