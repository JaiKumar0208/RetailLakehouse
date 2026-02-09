from typing import Optional, List
from sqlalchemy.orm import Session
from models.transactionsDetails.PurchaseOrder import PurchaseOrder
from datetime import datetime

class PurchaseOrderService:

    @staticmethod
    def create(
        db: Session,
        supplier_id: int,
        store_id: int,
        product_id: int,
        quantity: int,
        order_date,
        delivery_date=None
    ) -> PurchaseOrder:
        """Create a new purchase order"""
        po = PurchaseOrder(
            supplier_id=supplier_id,
            store_id=store_id,
            product_id=product_id,
            quantity=quantity,
            order_date=order_date,
            delivery_date=delivery_date
        )
        db.add(po)
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def get_by_id(db: Session, po_id: int) -> Optional[PurchaseOrder]:
        """Get purchase order by ID"""
        return db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()

    @staticmethod
    def get_all(db: Session) -> List[PurchaseOrder]:
        """Get all purchase orders"""
        return db.query(PurchaseOrder).all()

    @staticmethod
    def get_by_supplier(db: Session, supplier_id: int) -> List[PurchaseOrder]:
        """Get purchase orders for a supplier"""
        return db.query(PurchaseOrder).filter(PurchaseOrder.supplier_id == supplier_id).all()

    @staticmethod
    def get_by_store(db: Session, store_id: int) -> List[PurchaseOrder]:
        """Get purchase orders for a store"""
        return db.query(PurchaseOrder).filter(PurchaseOrder.store_id == store_id).all()

    @staticmethod
    def update(
        db: Session,
        po_id: int,
        quantity: int = None,
        delivery_date=None
    ) -> Optional[PurchaseOrder]:
        """Update purchase order details"""
        po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
        if not po:
            return None

        if quantity is not None:
            po.quantity = quantity
        if delivery_date is not None:
            po.delivery_date = delivery_date

        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def delete(db: Session, po_id: int) -> bool:
        """Delete purchase order"""
        po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
        if not po:
            return False

        db.delete(po)
        db.commit()
        return True

    @staticmethod
    def soft_delete_payment(db: Session, po_id: int):
        po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
        if po:
            po.deleted_at = datetime.now()
            db.commit()

