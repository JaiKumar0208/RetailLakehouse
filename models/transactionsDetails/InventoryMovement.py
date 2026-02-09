from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class InventoryMovement(Base, TimestampMixin):
    __tablename__ = "inventory_movements"
    __table_args__ = {"schema": "dbo"}
    movement_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("dbo.stores.store_id"))
    product_id = Column(Integer, ForeignKey("dbo.products.product_id"))
    quantity_change = Column(Integer)
    movement_type = Column(String(20))
    movement_date = Column(DateTime)

    store = relationship("Store", back_populates="inventory")
    product = relationship("Product", back_populates="inventory")

