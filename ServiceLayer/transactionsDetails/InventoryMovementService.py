from typing import Optional, List, Any
from sqlalchemy.orm import Session
from datetime import datetime
from models import InventoryMovement
from models.transactionsDetails.InventoryMovement import InventoryMovement


class InventoryMovementService:

    @staticmethod
    def create(
        db: Session,
        store_id: int,
        product_id: int,
        quantity_change: int,
        movement_type: str,
        movement_date
    ) -> InventoryMovement:
        """Create a new inventory movement record"""
        movement = InventoryMovement(
            store_id=store_id,
            product_id=product_id,
            quantity_change=quantity_change,
            movement_type=movement_type,
            movement_date=movement_date
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_by_id(db: Session, movement_id: int) -> Optional[InventoryMovement]:
        """Get movement by ID"""
        return db.query(InventoryMovement).filter(
            InventoryMovement.movement_id == movement_id
        ).first()

    @staticmethod
    def get_all(db: Session) -> list[type[InventoryMovement]]:
        """Get all inventory movements"""
        return db.query(InventoryMovement).all()

    @staticmethod
    def get_by_store(db: Session, store_id: int) -> list[type[InventoryMovement]]:
        """Get movements for a specific store"""
        return db.query(InventoryMovement).filter(
            InventoryMovement.store_id == store_id
        ).all()

    @staticmethod
    def get_by_product(db: Session, product_id: int) -> list[type[InventoryMovement]]:
        """Get movements for a specific product"""
        return db.query(InventoryMovement).filter(
            InventoryMovement.product_id == product_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        movement_id: int,
        quantity_change: int = None,
        movement_type: str = None,
        movement_date=None
    ) -> type[InventoryMovement] | None:
        """Update inventory movement"""
        movement = db.query(InventoryMovement).filter(
            InventoryMovement.movement_id == movement_id
        ).first()

        if not movement:
            return None

        if quantity_change is not None:
            movement.quantity_change = quantity_change
        if movement_type is not None:
            movement.movement_type = movement_type
        if movement_date is not None:
            movement.movement_date = movement_date

        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def delete(db: Session, movement_id: int) -> bool:
        """Delete inventory movement"""
        movement = db.query(InventoryMovement).filter(
            InventoryMovement.movement_id == movement_id
        ).first()

        if not movement:
            return False

        db.delete(movement)
        db.commit()
        return True

    @staticmethod
    def soft_delete_payment(db: Session, transaction_id: int):
        movement = db.query(InventoryMovement).filter(InventoryMovement.transaction_id == transaction_id).first()
        if movement:
            movement.deleted_at = datetime.now()
            db.commit()

