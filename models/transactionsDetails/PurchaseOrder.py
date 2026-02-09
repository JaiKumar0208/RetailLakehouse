from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class PurchaseOrder(Base, TimestampMixin):
    __tablename__ = "purchase_orders"
    po_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey("dbo.suppliers.supplier_id"))
    store_id = Column(Integer, ForeignKey("dbo.stores.store_id"))
    product_id = Column(Integer, ForeignKey("dbo.products.product_id"))
    quantity = Column(Integer)
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)

    supplier = relationship("Supplier", back_populates="purchase_orders")
    store = relationship("Store", back_populates="purchase_orders")
    product = relationship("Product", back_populates="purchase_orders")

