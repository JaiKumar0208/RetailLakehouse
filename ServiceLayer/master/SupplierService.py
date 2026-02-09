from typing import Optional, List
from sqlalchemy.orm import Session
from models.master.Supplier import Supplier
from datetime import datetime

class SupplierService:

    @staticmethod
    def create_supplier(
        db: Session,
        supplier_name: str,
        city: str = None
    ) -> Supplier:
        """Create a new supplier"""
        supplier = Supplier(
            supplier_name=supplier_name,
            city=city
        )
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def get_by_id_supplier(db: Session, supplier_id: int) -> Optional[Supplier]:
        """Get supplier by ID"""
        return db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()

    @staticmethod
    def get_all_supplier(db: Session) -> List[Supplier]:
        """Get all suppliers"""
        return db.query(Supplier).all()

    @staticmethod
    def get_by_city_supplier(db: Session, city: str) -> List[Supplier]:
        """Get suppliers from a specific city"""
        return db.query(Supplier).filter(Supplier.city == city).all()

    @staticmethod
    def update_supplier(
        db: Session,
        supplier_id: int,
        supplier_name: str = None,
        city: str = None
    ) -> Optional[Supplier]:
        """Update supplier details"""
        supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
        if not supplier:
            return None

        if supplier_name is not None:
            supplier.supplier_name = supplier_name
        if city is not None:
            supplier.city = city

        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def delete_supplier(db: Session, supplier_id: int) -> bool:
        """Delete a supplier"""
        supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
        if not supplier:
            return False

        db.delete(supplier)
        db.commit()
        return True

    @staticmethod
    def soft_delete_supplier(db: Session, supplier_id: int):
        supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
        if supplier:
            supplier.deleted_at = datetime.now()
            db.commit()