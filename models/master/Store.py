from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Store(Base, TimestampMixin):
    __tablename__ = "stores"
    __table_args__ = {"schema": "dbo"}
    store_id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String(100), nullable=False)
    city = Column(String(100))
    state = Column(String(50))
    open_date = Column(Date)

    employees = relationship("Employee", back_populates="store")
    sales = relationship("SalesTransaction", back_populates="store")
    inventory = relationship("InventoryMovement", back_populates="store")
    purchase_orders = relationship("PurchaseOrder", back_populates="store")