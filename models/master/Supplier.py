from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "dbo"}
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_name = Column(String(150))
    city = Column(String(100))

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
