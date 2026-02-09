from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Product(Base, TimestampMixin):
    __tablename__ = "products"
    __table_args__ = {"schema": "dbo"}
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(150), nullable=False)
    category = Column(String(100))
    sub_category = Column(String(100))
    price = Column(DECIMAL(10,2))

    sales = relationship("SalesTransaction", back_populates="product")
    inventory = relationship("InventoryMovement", back_populates="product")
    purchase_orders = relationship("PurchaseOrder", back_populates="product")
    returns = relationship("SalesReturn", back_populates="product")
